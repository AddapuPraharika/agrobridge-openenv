"""
AgroBridge OpenEnv — Inference Script
Meta × PyTorch OpenEnv Hackathon submission

This script runs a baseline LLM agent (Qwen2.5-72B-Instruct via HuggingFace
Inference Router) against the AgroBridgeEnv environment. The environment is
instantiated locally — no HTTP calls to the HF Space are required.

Usage:
    export HF_TOKEN=hf_...
    python inference.py
"""

import asyncio
import os
import textwrap
from typing import List, Optional

from openai import AsyncOpenAI  

from env import AgroBridgeEnv, MAX_STEPS
from models import AgroBridgeAction

# ── Configuration ──

API_KEY: str = os.getenv("HF_TOKEN") or os.getenv("API_KEY") or ""
API_BASE_URL: str = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME: str = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

TASK_NAME: str = os.getenv("TASK_NAME", "agrobridge")
BENCHMARK: str = os.getenv("BENCHMARK", "agrobridge-openenv")

TEMPERATURE: float = 0.7
MAX_TOKENS: int = 150
SUCCESS_SCORE_THRESHOLD: float = 0.5


SYSTEM_PROMPT = textwrap.dedent("""
    You are an AI agent for an agricultural labor marketplace in rural India.
    Your job is to assign the best available farmer to an agricultural job.

    Each farmer has:
    - A skill  (cotton | rice | spraying | tractor | water)
    - An experience level  (junior | senior)
    - Availability status

    Each job has:
    - A required skill
    - A difficulty level  (easy | medium | hard)
    - An urgency level    (LOW | MEDIUM | HIGH)

    Rules:
    - Always pick a farmer whose skill EXACTLY matches the required skill if possible.
    - For hard or high-urgency jobs, prefer SENIOR farmers.
    - Only pick AVAILABLE farmers listed in the observation.
    - Respond with the farmer's name and a brief reason.

    Example response:
    "Assign Ramesh because he is a senior cotton farmer and the job requires cotton skill."
""").strip()



def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(
    step: int, action: str, reward: float, done: bool, error: Optional[str]
) -> None:
    error_val = error if error else "null"
    action_clean = action.replace("\n", " ")[:80]
    print(
        f"[STEP] step={step} action={action_clean} "
        f"reward={reward:.2f} done={str(done).lower()} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}",
        flush=True,
    )


def build_user_prompt(
    step: int, last_obs: str, last_reward: float, history: List[str]
) -> str:
    history_block = "\n".join(history[-4:]) if history else "None"
    return textwrap.dedent(f"""
        Step: {step}

        Current situation:
        {last_obs}

        Last reward received: {last_reward:.2f}
        (1.0 = perfect match, 0.5 = partial match, 0.0 = wrong match or ambiguous action)

        Your previous actions:
        {history_block}

        Based on the job requirements and available farmers, assign the best farmer.
        Name the farmer explicitly and explain why.
    """).strip()



async def get_model_action(
    client: AsyncOpenAI,
    step: int,
    last_obs: str,
    last_reward: float,
    history: List[str],
) -> str:
    prompt = build_user_prompt(step, last_obs, last_reward, history)
    try:
        completion = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        action = completion.choices[0].message.content.strip()
        return action if action else "assign best available farmer"
    except Exception as exc:
        print(f"[DEBUG] Model error: {exc}", flush=True)
        return "assign best available farmer"



async def main() -> None:
    if not API_KEY:
        print(
            "[WARN] No HF_TOKEN or API_KEY found in environment. "
            "LLM calls will fail unless the router allows anonymous access.",
            flush=True,
        )

    client = AsyncOpenAI(base_url=API_BASE_URL, api_key=API_KEY or "anonymous")
    env = AgroBridgeEnv()

    history: List[str] = []
    rewards: List[float] = []
    steps_taken = 0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        result = await env.reset()
        last_obs = result.observation
        last_reward = 0.0

        for step in range(1, MAX_STEPS + 1):
            if result.done:
                break

            action_text = await get_model_action(
                client, step, last_obs, last_reward, history
            )

            result = await env.step(AgroBridgeAction(message=action_text))

            reward = result.reward
            done = result.done

            rewards.append(reward)
            steps_taken = step
            last_obs = result.observation
            last_reward = reward

            log_step(step=step, action=action_text, reward=reward, done=done, error=None)
            history.append(f"Step {step}: {action_text[:60]} -> reward {reward:.2f}")

            if done:
                break

        success = any(r >= SUCCESS_SCORE_THRESHOLD for r in rewards)

    except Exception as exc:
        print(f"[DEBUG] Episode error: {exc}", flush=True)

    finally:
        await env.close()
        log_end(success=success, steps=steps_taken, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())