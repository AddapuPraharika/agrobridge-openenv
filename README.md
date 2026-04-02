---

title: "AgroBridge OpenEnv"
emoji: "🌾"
colorFrom: "green"
colorTo: "blue"
sdk: "docker"
pinned: false
---

# AgroBridge OpenEnv

AgroBridge is an AI training environment that simulates matching farmers with agricultural jobs posted by landowners.

Landowners create agricultural tasks such as irrigation, rice planting, or pesticide spraying. Farmers with different skill sets are available to perform these tasks. The AI agent must assign the correct farmer to the correct job in order to maximize reward.

This environment simulates a real-world agricultural labor allocation system.

---

## Environment Overview

The environment follows the OpenEnv interface.

Main functions:

* reset() – Initializes the environment and returns the first observation
* step(action) – Executes an action and returns observation, reward, and done
* state() – Returns the current environment state

---

## Observation Space

The observation contains the current agricultural job requirements.

Example:

{
"job": {
"job": "pesticide spraying",
"required_skill": "spraying",
"difficulty": "hard"
}
}

---

## Action Space

The agent selects a farmer to assign to the job.

Example actions:

0 → Assign farmer with irrigation skill
1 → Assign farmer with rice farming skill
2 → Assign farmer with spraying skill

---

## Tasks

The environment includes three tasks:

Easy — Irrigation
Medium — Rice planting
Hard — Pesticide spraying

---

## Reward Function

Rewards measure how well the agent assigns farmers to jobs.

Correct assignment → reward between **0.5 – 1.0**

Partial match → reward between **0.2 – 0.4**

Incorrect assignment → reward **0**

---

## Deployment

The environment is deployed on **Hugging Face Spaces** using Docker.

The project includes:

* Dockerfile
* FastAPI server
* openenv.yaml configuration
* OpenEnv environment implementation

---

## Goal

The goal of the agent is to maximize reward by assigning the correct farmer to each agricultural task.

AgroBridge demonstrates how reinforcement learning environments can simulate real-world agricultural labor matching problems.
