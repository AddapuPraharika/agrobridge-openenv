---
title: AgroBridge OpenEnv
emoji: 🌾
colorFrom: green
colorTo: yellow
sdk: docker
pinned: false
---
🌾AgroBridge OpenEnv

AgroBridge OpenEnv is a reinforcement learning environment designed for intelligent agricultural labor matching in rural India.

Built using the OpenEnv framework for the Meta × PyTorch OpenEnv Hackathon.

🚨The Problem

India has 120 million agricultural laborers, the largest farm workforce in the world. Yet every harvest season:

30% of crops are lost due to labor shortages and incorrect skill assignments
Farmers lose approximately ₹1.5 lakh crore (~$18 billion) annually from harvest delays
74% of rural workers are mismatched to tasks outside their skill set

Agricultural job allocation is complex because:

Worker availability changes daily
Job urgency varies
Skill compatibility matters

Rule-based systems fail in such dynamic environments.

AgroBridge trains an AI agent to learn optimal labor assignments using reinforcement learning.

💡Solution

AgroBridge is a multi-step RL environment where an AI agent must assign the most suitable farmer to an agricultural job.

The agent learns that:

Exact skill matching gives maximum reward
Partial skill overlap gives partial reward
Experience level matters for difficult jobs
High urgency increases reward impact

The agent must operate under uncertain farmer availability and time constraints, making it a real RL decision problem.

🔁Environment API

The environment follows the OpenEnv standard.

Endpoint	Method	Description
/	GET	Health check
/reset	POST	Start a new episode
/step	POST	Assign a farmer and receive reward
/state	GET	View internal environment state
/close	POST	Close and reset the environment

👁️Observation Space

Each step returns a natural language observation:

Job: pesticide spraying
Description: Emergency pesticide spraying to control locust outbreak across 12 acres
Required skill: spraying
Difficulty: hard
Urgency: HIGH
Step: 1/3

Available farmers:
Ramesh (skill: cotton, level: senior)
Mahesh (skill: spraying, level: senior)
Dinesh (skill: tractor, level: junior)

The agent must reason about:

job requirements
farmer skills
urgency level
remaining steps
available workers

🎮Action Space

The agent responds with a natural language assignment.

Example:

{
  "message": "Assign Mahesh because he is a senior spraying expert and the job urgently requires pesticide spraying."
}

The environment extracts the farmer name and skill from the message.

🏆Reward Function

The reward function considers skill match, experience, and urgency.

Base Skill Match
Match Type	Reward
Exact skill	1.0
Same skill group	0.5
No match	0.0
Experience Bonus
Difficulty	Senior	Junior
Easy	+0.0	+0.0
Medium	+0.1	-0.1
Hard	+0.2	-0.2
Urgency Multiplier
Urgency	Multiplier
LOW	×1.0
MEDIUM	×1.1
HIGH	×1.2
Final Reward
final_reward = min(1.0, max(0.0, (base_reward + experience_bonus) * urgency_multiplier))

📋Tasks
Job	Skill	Difficulty	Urgency	Description
Cotton Harvesting	cotton	Easy	LOW	Harvest cotton before rainfall
Rice Planting	rice	Medium	MEDIUM	Plant paddy during monsoon
Pesticide Spraying	spraying	Hard	HIGH	Emergency pest control
Tractor Ploughing	tractor	Hard	MEDIUM	Prepare land before sowing
Irrigation Management	water	Medium	HIGH	Manage drip irrigation

👨‍🌾Farmer Pool
Name	Skill	Experience
Ramesh	cotton	Senior
Suresh	rice	Junior
Mahesh	spraying	Senior
Dinesh	tractor	Junior
Naresh	water	Senior
Lokesh	cotton	Junior
Ganesh	rice	Senior

Farmer availability is randomized each episode (70% probability).

🔄Multi-Step Episodes

Each episode has 3 steps.

Possible outcomes:

Perfect assignment → episode ends early
Suboptimal assignments → agent retries

Example:

Step 1 → wrong farmer → reward 0.0
Step 2 → partial match → reward 0.55
Step 3 → perfect match → reward 1.0

📊Example Output
[START] task=agrobridge env=agrobridge-openenv model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=Assign Mahesh reward=1.00 done=true
[END] success=true steps=1 rewards=1.00

🚀Setup
Run Locally
git clone https://huggingface.co/spaces/praharika18/agrobridge-openenv
cd agrobridge-openenv
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860
Run Inference
export HF_TOKEN=your_token
export API_BASE_URL=https://router.huggingface.co/v1
export MODEL_NAME=Qwen/Qwen2.5-72B-Instruct

python inference.py
Run with Docker
docker build -t agrobridge-openenv .

docker run -p 7860:7860 \
-e HF_TOKEN=your_token \
-e API_BASE_URL=https://router.huggingface.co/v1 \
-e MODEL_NAME=Qwen/Qwen2.5-72B-Instruct \
agrobridge-openenv

📁Project Structure
agrobridge-openenv/
│
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
🤖 Model & Infrastructure

Model: Qwen/Qwen2.5-72B-Instruct
API: OpenAI compatible client

Infrastructure:

CPU Basic (2 vCPU, 16GB RAM)
Runtime < 2 minutes
Max steps = 3

🌐Live Demo

https://praharika18-agrobridge-openenv.hf.space

👩‍💻Author

Addapu Praharika
B.Tech CSE (AI & ML)

Project created for the Meta × PyTorch OpenEnv Hackathon.

AgroBridge demonstrates how reinforcement learning can improve agricultural workforce allocation, impacting millions of farmers across rural India.