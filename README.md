---
title: AgroBridge OpenEnv
emoji: 🌾
colorFrom: green
colorTo: yellow
sdk: docker
pinned: false
---
🌾 AgroBridge OpenEnv

An OpenEnv reinforcement learning environment for intelligent agricultural labor matching in rural India.

Running on HF OpenEnv Spec Python

🚨The Problem

India has 120 million agricultural laborers — the largest farm workforce in the world. Yet every harvest season:

30% of crops are lost due to labor shortages and wrong skill assignments
Farmers lose an estimated ₹1.5 lakh crore (~$18 billion) annually from harvest delays
74% of rural job seekers are mismatched to tasks outside their skill set

No intelligent system exists to dynamically match workers to jobs based on skill, experience, and urgency.

This is not a simple scheduling problem. Farmer availability changes daily, job urgency varies, and skill compatibility is nuanced. A rule-based system breaks down immediately in real conditions.

AgroBridge teaches an AI agent to solve this matching problem optimally — learning from reward signals across thousands of episodes.

💡Solution

AgroBridge is a multi-step reinforcement learning environment built on the OpenEnv framework.

An AI agent:

Observes the current agricultural job
Evaluates available farmers by skill and experience
Assigns the best match

The agent learns:

Exact skill matching earns maximum reward
Partial skill overlap earns partial reward
Experience level matters for difficult jobs
High-urgency jobs amplify both rewards and penalties

Unlike a lookup table, the agent must handle dynamic farmer availability, varying urgency, and multi-step decision making — making this a genuine RL problem.

🔁Environment API

Fully compliant with the OpenEnv standard:

Endpoint	Method	Description
/	GET	Health check
/reset	POST	Start new episode — returns job observation
/step	POST	Assign a farmer — returns reward + next observation
/state	GET	Full environment state
/close	POST	Close and reset the environment
👁️Observation Space

Rich natural language observation given to the agent at each step:

Job: pesticide spraying.
Description: Emergency pesticide spraying to control locust outbreak across 12 acres.
Required skill: spraying. Difficulty: hard. Urgency: HIGH.
Step: 1/3.
Available farmers: Ramesh (skill:cotton, level:senior), Mahesh (skill:spraying, level:senior),
Dinesh (skill:tractor, level:junior)

The agent sees:

job details
urgency level
difficulty
step count
currently available farmers

This forces the agent to reason under real-world constraints.

🎮Action Space

The agent responds in natural language. The environment parses the farmer name and skill:

{
  "message": "Assign Mahesh because he is a senior spraying expert and the job urgently needs pesticide spraying."
}
🏆Reward Function

The reward function is difficulty-aware, experience-sensitive, and urgency-amplified.

Base Reward (Skill Match)
Match Type	Base Reward
Exact skill match	1.0
Same skill group (partial)	0.5
No match	0.0
Experience Bonus
Difficulty	Senior Farmer	Junior Farmer
Easy	+0.0	+0.0
Medium	+0.1	-0.1
Hard	+0.2	-0.2
Urgency Multiplier
Urgency	Multiplier
LOW (1)	×1.0
MEDIUM (2)	×1.1
HIGH (3)	×1.2
Final Reward Formula
final_reward = min(1.0, max(0.0, (base_reward + experience_bonus) × urgency_multiplier))
Example

Senior spraying farmer assigned to hard pesticide spraying with HIGH urgency:

base = 1.0
bonus = +0.2
multiplier = ×1.2

final = min(1.0, 1.2 × 1.2) = 1.0

Junior cotton farmer assigned to the same job:

base = 0.0
bonus = -0.2
multiplier = ×1.2

final = max(0.0, -0.24) = 0.0
📋Tasks
Job	Required Skill	Difficulty	Urgency	Description
Cotton Harvesting	cotton	Easy	LOW	Harvest mature cotton before rainfall
Rice Planting	rice	Medium	MEDIUM	Plant paddy within monsoon window
Pesticide Spraying	spraying	Hard	HIGH	Emergency locust outbreak control
Tractor Ploughing	tractor	Hard	MEDIUM	Deep ploughing before sowing season
Irrigation Management	water	Medium	HIGH	Manage drip irrigation for drought crops
👨‍🌾Farmer Pool
Name	Skill	Experience	Notes
Ramesh	cotton	Senior	Best for cotton tasks
Suresh	rice	Junior	Rice planting specialist
Mahesh	spraying	Senior	Expert in pesticide operations
Dinesh	tractor	Junior	Field machinery operator
Naresh	water	Senior	Irrigation management expert
Lokesh	cotton	Junior	Secondary cotton worker
Ganesh	rice	Senior	Experienced rice planting lead

Farmer availability is randomized each episode (70% probability available).

🔄Multi-Step Episode Design

Each episode runs up to 3 steps.

The episode ends when:

Reward ≥ 1.0 → success
3 steps exhausted

Example:

Episode Start → reset()

Step 1: wrong farmer → reward 0.0
Step 2: partial match → reward 0.55
Step 3: exact senior match → reward 1.0 → done
📊Sample Inference Output
[START] task=agrobridge env=agrobridge-openenv model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=Assign Mahesh, senior spraying expert for pesticide job reward=1.00 done=true error=null
[END] success=true steps=1 rewards=1.00
🚀Setup Instructions
Run Locally
git clone https://huggingface.co/spaces/praharika18/agrobridge-openenv
cd agrobridge-openenv
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860
Run Inference
export HF_TOKEN=your_hf_token
export API_BASE_URL=https://router.huggingface.co/v1
export MODEL_NAME=Qwen/Qwen2.5-72B-Instruct

python inference.py
Run with Docker
docker build -t agrobridge-openenv .

docker run -p 7860:7860 \
  -e HF_TOKEN=your_hf_token \
  -e API_BASE_URL=https://router.huggingface.co/v1 \
  -e MODEL_NAME=Qwen/Qwen2.5-72B-Instruct \
  agrobridge-openenv
📁File Structure
agrobridge-openenv/
├── app.py
├── env.py
├── models.py
├── graders.py
├── tasks.py
├── inference.py
├── openenv.yaml
├── Dockerfile
├── requirements.txt
└── README.md
🤖Model & Infrastructure

Model: Qwen/Qwen2.5-72B-Instruct via HuggingFace Router
API: OpenAI-compatible client

Infrastructure:

CPU Basic (2 vCPU, 16GB RAM)
Runtime < 2 minutes per episode
Max steps per episode: 3
🌐Live Demo

👉 https://praharika18-agrobridge-openenv.hf.space

👩‍💻Author

Built by Addapu Praharika for the Meta × PyTorch OpenEnv Hackathon organized by Scaler School of Technology.

AgroBridge addresses a real problem affecting 120 million agricultural workers in rural India, demonstrating how reinforcement learning can optimize real-world labor allocation systems.