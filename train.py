"""
AgroBridge OpenEnv — PyTorch Policy Training Script
Meta × PyTorch OpenEnv Hackathon

Trains a simple REINFORCE policy network to solve the AgroBridge farmer-matching
task. The policy takes a numeric feature vector encoding the current observation
and outputs a probability distribution over available farmers.

Usage:
    python train.py

The trained model is saved to: agrobridge_policy.pt
A reward curve is printed to stdout after training.
"""

import asyncio
import random
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim

from env import AgroBridgeEnv, MAX_STEPS
from graders import SKILL_GROUPS
from models import AgroBridgeAction

# ── Hyperparameters ──

EPISODES     = 800
LEARNING_RATE = 1e-3
GAMMA        = 0.99         # discount factor
HIDDEN_DIM   = 64
SAVE_PATH    = "agrobridge_policy.pt"
PRINT_EVERY  = 100

# ── Feature engineering ───

ALL_SKILLS    = ["cotton", "rice", "spraying", "tractor", "water"]
DIFFICULTIES  = ["easy", "medium", "hard"]
URGENCIES     = [1, 2, 3]


def skill_to_idx(skill: str) -> int:
    return ALL_SKILLS.index(skill) if skill in ALL_SKILLS else 0


def encode_observation(env: AgroBridgeEnv, farmer_idx: int) -> torch.Tensor:
    
    task = env.current_task
    farmer = env.farmers[farmer_idx]

    req_skill_idx   = skill_to_idx(task["required_skill"]) / max(len(ALL_SKILLS) - 1, 1)
    diff_idx        = DIFFICULTIES.index(task["difficulty"]) / max(len(DIFFICULTIES) - 1, 1)
    urgency_norm    = (task["urgency"] - 1) / max(len(URGENCIES) - 1, 1)
    farm_skill_idx  = skill_to_idx(farmer.skill) / max(len(ALL_SKILLS) - 1, 1)
    is_senior       = 1.0 if farmer.experience == "senior" else 0.0
    exact_match     = 1.0 if farmer.skill == task["required_skill"] else 0.0

    fgroup = next(
        (g for g, s in SKILL_GROUPS.items() if farmer.skill in s), None
    )
    rgroup = next(
        (g for g, s in SKILL_GROUPS.items() if task["required_skill"] in s), None
    )
    group_match = 1.0 if (fgroup is not None and fgroup == rgroup) else 0.0
    available   = 1.0 if farmer.available else 0.0

    return torch.tensor(
        [req_skill_idx, diff_idx, urgency_norm, farm_skill_idx,
         is_senior, exact_match, group_match, available],
        dtype=torch.float32,
    )


# ── Policy network ───

class AgroBridgePolicyNet(nn.Module):
   

    def __init__(self, input_dim: int = 8, hidden_dim: int = HIDDEN_DIM) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(-1)

    def select_action(
        self, env: AgroBridgeEnv
    ) -> tuple[int, torch.Tensor]:
       
        available_indices = [i for i, f in enumerate(env.farmers) if f.available]
        if not available_indices:
            
            return 0, torch.tensor(0.0)

        features = torch.stack([
            encode_observation(env, i) for i in available_indices
        ])                                

        scores = self.forward(features)   
        probs  = torch.softmax(scores, dim=0)
        dist   = torch.distributions.Categorical(probs)
        local_idx = dist.sample()

        farmer_idx = available_indices[local_idx.item()]
        log_prob   = dist.log_prob(local_idx)
        return farmer_idx, log_prob


# ── REINFORCE training loop ────

def compute_returns(rewards: list[float], gamma: float) -> list[float]:
    returns: list[float] = []
    g = 0.0
    for r in reversed(rewards):
        g = r + gamma * g
        returns.insert(0, g)
    return returns


async def run_episode(
    env: AgroBridgeEnv, policy: AgroBridgePolicyNet
) -> tuple[list[float], list[torch.Tensor]]:
    result = await env.reset()
    ep_rewards: list[float] = []
    ep_log_probs: list[torch.Tensor] = []

    for _ in range(MAX_STEPS):
        if result.done:
            break

        farmer_idx, log_prob = policy.select_action(env)
        farmer = env.farmers[farmer_idx]
        message = f"Assign {farmer.name} because of skill match."
        result = await env.step(AgroBridgeAction(message=message))

        ep_rewards.append(result.reward)
        ep_log_probs.append(log_prob)

        if result.done:
            break

    return ep_rewards, ep_log_probs


async def train() -> AgroBridgePolicyNet:
    env    = AgroBridgeEnv()
    policy = AgroBridgePolicyNet()
    optimiser = optim.Adam(policy.parameters(), lr=LEARNING_RATE)

    print(f"Training AgroBridgePolicyNet for {EPISODES} episodes...")
    print(f"  Hidden dim : {HIDDEN_DIM}")
    print(f"  LR         : {LEARNING_RATE}")
    print(f"  Gamma      : {GAMMA}")
    print(f"  Device     : cpu (MPS/CUDA can be added trivially)\n")

    rolling_reward = 0.0
    best_avg = -1.0

    for ep in range(1, EPISODES + 1):
        ep_rewards, ep_log_probs = await run_episode(env, policy)

        if not ep_log_probs:
            continue

        returns = compute_returns(ep_rewards, GAMMA)
        returns_t = torch.tensor(returns, dtype=torch.float32)

        
        if returns_t.std() > 1e-8:
            returns_t = (returns_t - returns_t.mean()) / (returns_t.std() + 1e-8)

        
        loss = -torch.stack(ep_log_probs) @ returns_t

        optimiser.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(policy.parameters(), max_norm=1.0)
        optimiser.step()

        ep_total = sum(ep_rewards)
        rolling_reward = 0.95 * rolling_reward + 0.05 * ep_total

        if ep % PRINT_EVERY == 0:
            print(
                f"  Episode {ep:>4d}/{EPISODES}  "
                f"ep_reward={ep_total:.3f}  "
                f"rolling_avg={rolling_reward:.3f}  "
                f"loss={loss.item():.4f}"
            )
            if rolling_reward > best_avg:
                best_avg = rolling_reward
                torch.save(policy.state_dict(), SAVE_PATH)
                print(f"             ✓ New best ({best_avg:.3f}) — saved to {SAVE_PATH}")

    await env.close()
    print(f"\nTraining complete. Best rolling reward: {best_avg:.3f}")
    print(f"Model saved to: {SAVE_PATH}")
    return policy


async def evaluate(policy: AgroBridgePolicyNet, n_episodes: int = 100) -> None:
    """Evaluate the trained policy and print statistics."""
    env = AgroBridgeEnv()
    rewards: list[float] = []
    perfect = 0

    for _ in range(n_episodes):
        ep_rewards, _ = await run_episode(env, policy)
        total = sum(ep_rewards)
        rewards.append(total)
        if max(ep_rewards, default=0) >= 1.0:
            perfect += 1

    await env.close()
    avg  = sum(rewards) / max(len(rewards), 1)
    rate = perfect / max(n_episodes, 1) * 100
    print(f"\nEvaluation over {n_episodes} episodes:")
    print(f"  Avg total reward  : {avg:.3f}")
    print(f"  Perfect-match rate: {rate:.1f}%")


if __name__ == "__main__":
    async def _main():
        policy = await train()
        saved = Path(SAVE_PATH)
        if saved.exists():
            policy.load_state_dict(torch.load(SAVE_PATH, weights_only=True))
            policy.eval()
        await evaluate(policy)

    asyncio.run(_main())