---
title: AgroBridge OpenEnv
emoji: 🌾
colorFrom: green
colorTo: yellow
sdk: docker
pinned: true
---
# 🌾 AgroBridge OpenEnv

> **A reinforcement learning environment for intelligent agricultural labor matching in rural India — built on the OpenEnv framework for the Meta × PyTorch OpenEnv Hackathon.**

[![HuggingFace Space](https://img.shields.io/badge/🤗%20HuggingFace-Space-blue)](https://huggingface.co/spaces/praharika18/agrobridge-openenv)
[![OpenEnv Compliant](https://img.shields.io/badge/OpenEnv-Compliant-green)](https://github.com/meta-pytorch/OpenEnv)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📌 Problem Statement

India has **120 million agricultural laborers** — the largest farm workforce in the world. Yet every harvest season:

- **30% of crops are lost** due to labor shortages and wrong skill assignments
- Farmers lose an estimated **₹1.5 lakh crore (~$18 billion)** annually from harvest delays
- **74% of rural job seekers** are mismatched to tasks outside their skill set
- No intelligent system exists to dynamically match workers to jobs based on skill, experience, and urgency

This is not a simple scheduling problem. Farmer availability changes daily, job urgency varies, and skill compatibility is nuanced. A rule-based system breaks down immediately in real conditions.

**AgroBridge provides a reinforcement learning environment where agents can be trained and evaluated to solve this matching problem.**

---

## 💡 Solution Overview

AgroBridge is a **multi-step reinforcement learning environment** built on the OpenEnv framework. An AI agent observes the current agricultural job, evaluates available farmers by skill and experience, and assigns the best match.

The agent learns:

- Exact skill matching earns maximum reward
- Partial skill overlap earns partial reward
- Experience level matters for difficult jobs
- High-urgency jobs amplify both rewards and penalties

Unlike a lookup table, the agent must handle **dynamic farmer availability**, **varying urgency**, and **multi-step decision making** — making this a genuine RL problem.

---

## 🔁 Environment API

Fully compliant with the OpenEnv standard. All endpoints are served via FastAPI on port `7860`.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check — returns `{"status": "running"}` |
| `/reset` | POST | Start a new episode — returns initial observation |
| `/step` | POST | Assign a farmer — returns reward, next observation, and done flag |
| `/state` | GET | Full environment state including farmers and episode progress |
| `/close` | POST | Close and reset the environment cleanly |

---

## 👁️ Observation Space

**Type:** `string` (natural language)

At each step, the agent receives a structured natural language observation:

```
Job: pesticide spraying.
Description: Emergency pesticide spraying to control locust outbreak across 12 acres.
Required skill: spraying. Difficulty: hard. Urgency: HIGH.
Step: 1/3.
Available farmers: Ramesh (skill:cotton, level:senior), Mahesh (skill:spraying, level:senior), Dinesh (skill:tractor, level:junior).
```

The agent sees: job details, urgency level, difficulty, step count, and only the currently **available** farmers — forcing it to reason under real-world constraints.

---

## 🎮 Action Space

**Type:** `string` (natural language message)

The agent responds in natural language. The environment parses the farmer name and skill from the message.

**Request body:**

```json
{
  "message": "Assign Mahesh because he is a senior spraying expert and the job urgently needs pesticide spraying."
}
```

**Response:**

```json
{
  "observation": "Episode complete. Assigned Mahesh (skill:spraying, level:senior) to 'pesticide spraying'. Final reward: 1.00. Total episode rewards: [1.0].",
  "reward": 1.0,
  "done": true
}
```

---

## 🏆 Reward Function

The reward function is **difficulty-aware**, **experience-sensitive**, and **urgency-amplified**.

### Base Reward — Skill Match

| Match Type | Base Reward |
|------------|-------------|
| Exact skill match | `1.0` |
| Same skill group (partial match) | `0.5` |
| No match | `0.0` |

### Skill Groups

| Group | Skills |
|-------|--------|
| `crop` | cotton, rice |
| `field_ops` | spraying, tractor |
| `resource` | water |

### Experience Bonus — Applied by Difficulty

| Difficulty | Senior Farmer | Junior Farmer |
|------------|--------------|---------------|
| Easy | +0.0 | +0.0 |
| Medium | +0.1 | −0.1 |
| Hard | +0.2 | −0.2 |

### Urgency Multiplier

| Urgency | Multiplier |
|---------|------------|
| LOW (1) | ×1.0 |
| MEDIUM (2) | ×1.1 |
| HIGH (3) | ×1.2 |

### Final Reward Formula

```
final_reward = min(1.0, max(0.0, (base_reward + experience_bonus) × urgency_multiplier))
```

### Examples

**Best case** — senior spraying farmer on hard pesticide spraying with HIGH urgency:

```
base      = 1.0  (exact skill match)
bonus     = +0.2 (senior on hard task)
multiplier = ×1.2 (HIGH urgency)
final     = min(1.0, 1.2 × 1.2) = 1.0  ✅
```

**Worst case** — junior cotton farmer on the same task:

```
base      = 0.0  (no match)
bonus     = −0.2 (junior on hard task)
multiplier = ×1.2
final     = max(0.0, −0.24) = 0.0  ❌
```

---

## 📋 Tasks

| Job | Required Skill | Difficulty | Urgency | Description |
|-----|---------------|------------|---------|-------------|
| Cotton Harvesting | cotton | Easy | LOW | Harvest mature cotton from 5-acre field before rainfall |
| Rice Planting | rice | Medium | MEDIUM | Plant paddy seedlings across flooded fields within monsoon window |
| Pesticide Spraying | spraying | Hard | HIGH | Emergency pesticide spraying to control locust outbreak across 12 acres |
| Tractor Ploughing | tractor | Hard | MEDIUM | Deep ploughing of hard soil before sowing season begins |
| Irrigation Management | water | Medium | HIGH | Manage drip irrigation channels for drought-affected crops urgently |

---

## 👨‍🌾 Farmer Pool

| Name | Skill | Experience | Notes |
|------|-------|------------|-------|
| Ramesh | cotton | Senior | Best match for cotton harvesting tasks |
| Suresh | rice | Junior | Rice planting specialist |
| Mahesh | spraying | Senior | Expert in pesticide and spray operations |
| Dinesh | tractor | Junior | Field machinery operator |
| Naresh | water | Senior | Irrigation management expert |
| Lokesh | cotton | Junior | Secondary cotton worker |
| Ganesh | rice | Senior | Experienced rice planting lead |

Farmer **availability is randomized at the start of each episode** (70% chance available per farmer). If all farmers are unavailable, at least one is forced available. The agent must work with whoever is present — this is the core RL challenge.

---

## 🔄 Multi-Step Episode Design

Each episode runs for up to **3 steps**. The episode terminates early if the agent achieves a perfect reward (`≥ 1.0`).

```
Episode Start
     │
     ▼
  reset()  ──► Initial Observation (job + available farmers)
     │
     ▼
  Step 1:  Agent picks wrong farmer  ──► reward: 0.00  ──► try again
     │
     ▼
  Step 2:  Agent picks partial match ──► reward: 0.55  ──► try again
     │
     ▼
  Step 3:  Agent picks exact senior match ──► reward: 1.00  ──► done ✅
```

This multi-step design forces the agent to **learn from suboptimal assignments** and improve — genuine reinforcement learning behaviour.

---

## 📊 Example Inference Output

```
[START] task=agrobridge env=agrobridge-openenv model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=Assign Mahesh because he is a senior spraying expert reward=1.00 done=true error=null
[END] success=true steps=1 rewards=1.00
```

## 🔥 PyTorch Training

AgroBridge includes a PyTorch training example (`train.py`) that trains a policy network (`AgroBridgePolicyNet`) using the REINFORCE algorithm.

This demonstrates how reinforcement learning agents can be trained on the AgroBridge OpenEnv environment.

Example:

```bash
python train.py

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.10+
- Git
- Docker (optional, for containerised deployment)
- A Hugging Face account and `HF_TOKEN`

### Run Locally

```bash
# Clone the repository
git clone https://huggingface.co/spaces/praharika18/agrobridge-openenv
cd agrobridge-openenv

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app:app --host 0.0.0.0 --port 7860
```

The API will be available at `http://localhost:7860`.

### Run Inference

```bash
# Set environment variables
export HF_TOKEN=your_hf_token_here
export API_BASE_URL=https://router.huggingface.co/v1
export MODEL_NAME=Qwen/Qwen2.5-72B-Instruct

# Run the baseline inference agent
python inference.py
```

### Test the API Manually

```bash
# Health check
curl http://localhost:7860/

# Reset the environment
curl -X POST http://localhost:7860/reset

# Take a step
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{"message": "Assign Mahesh because he is a senior spraying expert."}'

# Get full environment state
curl http://localhost:7860/state

# Close the environment
curl -X POST http://localhost:7860/close
```

---

## 🐳 Docker Instructions

### Build and Run

```bash
# Build the Docker image
docker build -t agrobridge-openenv .

# Run the container
docker run -p 7860:7860 \
  -e HF_TOKEN=your_hf_token_here \
  -e API_BASE_URL=https://router.huggingface.co/v1 \
  -e MODEL_NAME=Qwen/Qwen2.5-72B-Instruct \
  agrobridge-openenv
```

### Run Inference Inside Docker

```bash
docker run --rm \
  -e HF_TOKEN=your_hf_token_here \
  -e API_BASE_URL=https://router.huggingface.co/v1 \
  -e MODEL_NAME=Qwen/Qwen2.5-72B-Instruct \
  agrobridge-openenv python inference.py
```

---

## 📁 Project Structure

```
agrobridge-openenv/
├── app.py            # FastAPI server — OpenEnv-compliant REST endpoints
├── env.py            # Core RL environment (multi-step, availability, urgency)
├── models.py         # Pydantic typed models (AgroBridgeAction, StepResult)
├── graders.py        # Difficulty-aware, experience-sensitive reward logic
├── tasks.py          # 20 realistic agricultural tasks with difficulty and urgency levels
├── inference.py      # Baseline agent using Qwen2.5-72B via HF Inference Router
├── train.py           # PyTorch REINFORCE training example
├── openenv.yaml      # OpenEnv specification file
├── Dockerfile        # Container definition — Python 3.10, uvicorn
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## 🤖 Model & Infrastructure

| Property | Value |
|----------|-------|
| Model | `Qwen/Qwen2.5-72B-Instruct` |
| API Client | OpenAI-compatible (`openai` Python SDK) |
| API Base | HuggingFace Inference Router (`router.huggingface.co/v1`) |
| Hardware | CPU Basic — 2 vCPU, 16 GB RAM |
| Inference Runtime | < 2 minutes per episode |
| Max Steps per Episode | 3 (configurable via `MAX_STEPS` in `env.py`) |
| Reward Range | `[0.0, 1.0]` |
| Framework | FastAPI + Uvicorn |
| Container | Docker (Python 3.10 base) |

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HF_TOKEN` | Hugging Face API key | — |
| `API_BASE_URL` | LLM API endpoint | `https://router.huggingface.co/v1` |
| `MODEL_NAME` | Model identifier | `Qwen/Qwen2.5-72B-Instruct` |

---

## 🚀 Live API

**API Status**
https://praharika18-agrobridge-openenv.hf.space

## 📘 API Documentation (Swagger)

Interactive Swagger documentation is available here:

https://praharika18-agrobridge-openenv.hf.space/docs

Using Swagger, you can directly test the API endpoints such as:

* `POST /reset` → Reset the RL environment
* `POST /step` → Perform an action in the environment
* `GET /state` → Retrieve the current environment state
* `POST /close` → Close the environment

This interface allows developers and evaluators to interact with the AgroBridge OpenEnv environment without writing any code.

---

## 🌐 Live Demo

👉 **[https://praharika18-agrobridge-openenv.hf.space](https://praharika18-agrobridge-openenv.hf.space)**

The environment is deployed as a Docker-based Hugging Face Space. It wakes automatically when pinged and responds to all OpenEnv API calls.

---

## 👩‍💻 Author

**Praharika** — B.Tech Computer Science (AI & ML), Malla Reddy Engineering College for Women, Hyderabad

Built for the **Meta × PyTorch OpenEnv Hackathon** organised by Scaler School of Technology.

> *AgroBridge addresses a real problem affecting 120 million lives in rural India — proving that reinforcement learning can bring intelligence to one of the world's oldest industries.*
