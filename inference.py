"""
AgroBridge OpenEnv — Inference Script
Meta x PyTorch OpenEnv Hackathon submission
"""

import asyncio
import os
import textwrap
from typing import List, Optional

from openai import OpenAI

from env import AgroBridgeEnv, MAX_STEPS
from models import AgroBridgeAction


API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

TASK_NAME = os.getenv("TASK_NAME", "agrobridge")
BENCHMARK = os.getenv("BENCHMARK", "agrobridge-openenv")

TEMPERATURE = 0.7
MAX_TOKENS = 150
SUCCESS_SCORE_THRESHOLD = 0.5

SYSTEM_PROMPT = textwrap.dedent("""
    You are an AI agent for an agricultural labor marketplace in rural India.

    Your job is to assign the best available farmer to an agricultural job.

    Each farmer has:
    - A skill (cotton, rice, spraying, tractor, water)
    - An experience level (junior or senior)
    - Availability status

    Each job has:
    - A required skill
    - A difficulty level (easy, medium, hard)
    - An urgency level (LOW, MEDIUM, HIGH)

    Rules:
    - Always pick a farmer whose skill EXACTLY matches the required skill if possible.
    - For hard or high-urgency jobs, prefer SENIOR farmers.
    - Only pick AVAILABLE farmers.
    - Respond with the farmer's name and a brief reason.

    Example response:
    "Assign Ramesh because he is a senior cotton farmer and the job requires cotton skill urgently."
""").strip()


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    action_clean = action.replace("\n", " ")[:80]
    print(
        f"[STEP] step={step} action={action_clean} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}",
        flush=True,
    )


def build_user_prompt(step: int, last_obs: str, last_reward: float, history: List[str]) -> str:
    history_block = "\n".join(history[-4:]) if history else "None"
    return textwrap.dedent(f"""
        Step: {step}

        Current situation:
        {last_obs}

        Last reward received: {last_reward:.2f}
        (1.0 = perfect match, 0.5 = partial match, 0.0 = wrong match)

        Your previous actions:
        {history_block}

        Based on the job requirements and available farmers, assign the best farmer.
        Name the farmer explicitly and explain why.
    """).strip()


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
        return action if action else "assign best available farmer"
    except Exception as e:
        print(f"[DEBUG] Model error: {e}", flush=True)
        return "assign best available farmer"


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

            action_text = get_model_action(client, step, last_obs, last_reward, history)
            result = await env.step(AgroBridgeAction(message=action_text))

            reward = result.reward or 0.0
            done = result.done

            rewards.append(reward)
            steps_taken = step
            last_obs = str(result.observation)
            last_reward = reward

            log_step(step=step, action=action_text, reward=reward, done=done, error=None)
            history.append(f"Step {step}: {action_text[:60]} -> reward {reward:.2f}")

            if done:
                break

        success = any(r >= SUCCESS_SCORE_THRESHOLD for r in rewards)

    except Exception as e:
        print(f"[DEBUG] Episode error: {e}", flush=True)
    finally:
        await env.close()

    log_end(success=success, steps=steps_taken, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())