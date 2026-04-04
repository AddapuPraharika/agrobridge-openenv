---
title: AgroBridge OpenEnv
emoji: 🌾
colorFrom: green
colorTo: yellow
sdk: docker
pinned: false
---

# 🌾 AgroBridge OpenEnv

An OpenEnv-compatible reinforcement learning environment that simulates **real-world agricultural job matching** — assigning the right farmer to the right job based on skills, availability, and task difficulty.

---

## 📌 What is AgroBridge?

AgroBridge is a real-world RL environment where an AI agent learns to **match farmers to agricultural jobs** based on skill compatibility. The agent receives job descriptions, evaluates available farmers, and assigns the best match — receiving rewards based on how well the assignment fits.

This simulates a real problem faced in rural India and other agricultural economies where labor marketplaces need intelligent job-worker matching.

---

## 🔁 Environment API

This environment follows the standard OpenEnv spec:

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Health check — returns running status |
| `/reset` | POST | Resets the environment, returns new job observation |
| `/step` | POST | Takes an action (farmer assignment), returns reward |
| `/state` | GET | Returns current job and available farmers |

---

## 👁️ Observation Space

Each observation is a natural language string describing the current job and available farmers. Example:

```
Job: cotton harvesting. Required skill: cotton. Difficulty: easy.
Available farmers: Ramesh (cotton), Suresh (rice), Mahesh (spraying), Dinesh (tractor), Naresh (water)
```

---

## 🎮 Action Space

The agent sends a natural language message naming the farmer it wants to assign. Example:

```json
{"message": "Assign Ramesh because his cotton skill matches the cotton harvesting job."}
```

The environment parses the farmer name or skill from the message and grades the assignment.

---

## 🏆 Reward Function

| Situation | Reward |
|---|---|
| Farmer skill exactly matches job | `1.0` |
| Farmer skill is in the same skill group | `0.5` |
| Farmer skill does not match at all | `0.0` |

**Skill Groups:**
- Crop group: `cotton`, `rice`
- Field ops group: `spraying`, `tractor`
- Resource group: `water`

---

## 📋 Tasks

| Task | Required Skill | Difficulty |
|---|---|---|
| Cotton Harvesting | cotton | Easy |
| Rice Planting | rice | Medium |
| Pesticide Spraying | spraying | Hard |
| Tractor Ploughing | tractor | Hard |
| Irrigation Management | water | Medium |

---

## 👨‍🌾 Available Farmers

| Name | Skill |
|---|---|
| Ramesh | cotton |
| Suresh | rice |
| Mahesh | spraying |
| Dinesh | tractor |
| Naresh | water |

---

## 🚀 Setup Instructions

### 1. Clone the Space
```bash
git clone https://huggingface.co/spaces/praharika18/agrobridge-openenv
cd agrobridge-openenv
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Environment Locally
```bash
uvicorn app:app --host 0.0.0.0 --port 7860
```

### 4. Run Inference Script
```bash
export HF_TOKEN=your_hf_token
export API_BASE_URL=https://router.huggingface.co/v1
export MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
python inference.py
```

### 5. Run with Docker
```bash
docker build -t agrobridge-openenv .
docker run -p 7860:7860 \
  -e HF_TOKEN=your_hf_token \
  -e API_BASE_URL=https://router.huggingface.co/v1 \
  -e MODEL_NAME=Qwen/Qwen2.5-72B-Instruct \
  agrobridge-openenv
```

---

## 📦 Requirements

```
fastapi
uvicorn
openai
```

---

## 🌐 Live Demo

👉 [https://praharika18-agrobridge-openenv.hf.space](https://praharika18-agrobridge-openenv.hf.space)

---

## 📁 File Structure

```
agrobridge-openenv/
├── app.py          # FastAPI server with OpenEnv endpoints
├── env.py          # Core RL environment logic
├── models.py       # Typed data models
├── graders.py      # Reward/grading functions
├── tasks.py        # Task definitions
├── inference.py    # Baseline inference script
├── openenv.yaml    # OpenEnv specification
├── Dockerfile      # Container configuration
├── requirements.txt
└── README.md
```

---

## 🤖 Model Used

- **Model:** `Qwen/Qwen2.5-72B-Instruct`
- **API:** HuggingFace Inference Router (OpenAI-compatible)
- **Max Steps:** 8 per episode
- **Temperature:** 0.7

---

## 👩‍💻 Author

Built for the **Meta x PyTorch OpenEnv Hackathon** by Scaler School of Technology.
