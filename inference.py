"""
AgroBridge OpenEnv Inference Script
Required for OpenEnv Hackathon evaluation
"""

import asyncio
import os
import textwrap
from typing import List, Optional

from openai import OpenAI

from env import AgroBridgeEnv
from models import AgroBridgeAction


# ==============================
# Environment Variables
# ==============================

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

TASK_NAME = os.getenv("TASK_NAME", "agrobridge")
BENCHMARK = os.getenv("BENCHMARK", "agrobridge-openenv")

MAX_STEPS = 8
TEMPERATURE = 0.7
MAX_TOKENS = 120
SUCCESS_SCORE_THRESHOLD = 0.1


# ==============================
# System Prompt
# ==============================

SYSTEM_PROMPT = textwrap.dedent(
    """
    You are an AI agent helping match farmers with agricultural jobs.

    Each job requires a specific skill such as:
    - cotton (cotton harvesting)
    - rice (rice planting)
    - spraying (pesticide spraying)
    - tractor (tractor ploughing)
    - water (irrigation management)

    Available farmers and their skills will be shown to you.
    Your goal is to assign the best matching farmer to the job.

    Respond with the farmer's name and reason for assignment. Example:
    "Assign Ramesh because his cotton skill matches the cotton harvesting job."
    """
).strip()


# ==============================
# Logging Functions (MANDATORY)
# ==============================

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}",
        flush=True,
    )


# ==============================
# Prompt Builder
# ==============================

def build_user_prompt(step: int, last_obs: str, last_reward: float, history: List[str]) -> str:
    history_block = "\n".join(history[-4:]) if history else "None"
    return textwrap.dedent(
        f"""
        Step: {step}

        Current observation:
        {last_obs}

        Last reward: {last_reward}

        Previous actions:
        {history_block}

        Choose the best farmer to assign to this job. Mention the farmer's name.
        """
    ).strip()


# ==============================
# Model Call
# ==============================

def get_model_action(client, step, last_obs, last_reward, history):
    prompt = build_user_prompt(step, last_obs, last_reward, history)
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        action = completion.choices[0].message.content.strip()
        return action if action else "assign farmer"
    except Exception as e:
        print(f"[DEBUG] Model error: {e}", flush=True)
        return "assign farmer"


# ==============================
# Main Execution
# ==============================

async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    env = AgroBridgeEnv()

    history: List[str] = []
    rewards: List[float] = []

    steps_taken = 0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        result = await env.reset()

        last_obs = str(result.observation)
        last_reward = 0.0

        for step in range(1, MAX_STEPS + 1):

            if result.done:
                break

            action_text = get_model_action(
                client, step, last_obs, last_reward, history
            )

            result = await env.step(AgroBridgeAction(message=action_text))

            reward = result.reward or 0.0
            done = result.done

            rewards.append(reward)
            steps_taken = step

            last_obs = str(result.observation)
            last_reward = reward

            log_step(step=step, action=action_text, reward=reward, done=done, error=None)

            history.append(f"Step {step}: {action_text} -> reward {reward}")

            if done:
                break

        success = any(r >= SUCCESS_SCORE_THRESHOLD for r in rewards)

    finally:
        pass

    log_end(success=success, steps=steps_taken, rewards=rewards)


# ==============================
# Run
# ==============================

if __name__ == "__main__":
    asyncio.run(main())
