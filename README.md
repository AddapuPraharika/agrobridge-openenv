---
title: AgroBridge OpenEnv
emoji: 🌾
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---
---

title: AgroBridge OpenEnv
emoji: 🌾
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
-------------

# AgroBridge OpenEnv

AgroBridge is an AI training environment that simulates matching farmers with agricultural jobs posted by landowners.

Landowners create agricultural tasks such as irrigation, harvesting, or pesticide spraying. Farmers with different skill sets are available to perform these tasks. The goal of the AI agent is to assign the correct farmer to the correct job in order to maximize reward.

This environment simulates a real-world agricultural labor matching system.

---

# Environment Overview

The agent interacts with the environment using the standard OpenEnv interface.

The main functions are:

reset() → Initializes the environment and returns the first observation.

step(action) → Executes the agent's action and returns observation, reward, and done status.

state() → Returns the current state of the environment.

---

# Observation Space

The observation contains the current job requirements.

Example observation returned by the environment:

{
"job": {
"job": "pesticide spraying",
"required_skill": "spraying",
"difficulty": "hard"
}
}

The observation includes:

Job type
Required skill
Task difficulty

---

# Action Space

The agent selects a farmer to assign to the job.

Example action mapping:

0 → Assign farmer with cotton farming skill
1 → Assign farmer with rice farming skill
2 → Assign farmer with pesticide spraying skill

The agent must select the correct farmer whose skill matches the job requirement.

---

# Tasks

The environment includes multiple agricultural tasks with increasing difficulty.

Easy Task
Irrigation task requiring basic farming knowledge.

Medium Task
Rice planting requiring crop-specific expertise.

Hard Task
Pesticide spraying requiring specialized spraying skill.

These tasks simulate real-world agricultural work scenarios.

---

# Reward Function

The reward function measures how well the agent assigns farmers to jobs.

Correct farmer assignment
Reward between 0.5 and 1.0

Partial skill match
Reward between 0.2 and 0.4

Incorrect assignment
Reward 0

The agent learns to maximize reward by selecting the correct farmer for each job.

---

# Example Environment Output

Example response returned by the environment:

{
"job": {
"job": "pesticide spraying",
"required_skill": "spraying",
"difficulty": "hard"
},
"reward": 0.5,
"done": true
}

This indicates the environment evaluated the agent's action and returned the corresponding reward.

---

# Deployment

The environment is containerized using Docker and deployed on Hugging Face Spaces.

The project includes:

Dockerfile
openenv.yaml configuration
FastAPI server
OpenEnv environment implementation

This ensures the environment can be automatically validated and executed by the evaluation system.

---

# Goal of the Environment

The objective of the agent is to maximize total reward by learning optimal job assignments between farmers and agricultural tasks.

This environment demonstrates how reinforcement learning agents can assist in real-world agricultural labor allocation problems.
