import random
from tasks import tasks
from models import Farmer, AgroBridgeAction, StepResult
from graders import grade_assignment

MAX_STEPS = 3


class AgroBridgeEnv:

    def __init__(self):
        self.farmers = [
            Farmer("Ramesh", "cotton",   experience="senior", available=True),
            Farmer("Suresh", "rice",     experience="junior", available=True),
            Farmer("Mahesh", "spraying", experience="senior", available=True),
            Farmer("Dinesh", "tractor",  experience="junior", available=True),
            Farmer("Naresh", "water",    experience="senior", available=True),
            Farmer("Lokesh", "cotton",   experience="junior", available=True),
            Farmer("Ganesh", "rice",     experience="senior", available=True),
        ]
        self.current_task = None
        self.step_count = 0
        self.max_steps = MAX_STEPS
        self.episode_rewards = []

    def _randomize_availability(self):
        for farmer in self.farmers:
            farmer.available = random.random() > 0.3
        if not any(f.available for f in self.farmers):
            self.farmers[0].available = True

    def _build_observation(self) -> str:
        available = [f for f in self.farmers if f.available]
        farmer_list = ", ".join(
            f"{f.name} (skill:{f.skill}, level:{f.experience})"
            for f in available
        )
        urgency_label = {1: "LOW", 2: "MEDIUM", 3: "HIGH"}[self.current_task["urgency"]]
        return (
            f"Job: {self.current_task['job']}. "
            f"Description: {self.current_task['description']} "
            f"Required skill: {self.current_task['required_skill']}. "
            f"Difficulty: {self.current_task['difficulty']}. "
            f"Urgency: {urgency_label}. "
            f"Step: {self.step_count + 1}/{self.max_steps}. "
            f"Available farmers: {farmer_list}."
        )

    async def reset(self) -> StepResult:
        self.current_task = random.choice(tasks)
        self.step_count = 0
        self.episode_rewards = []
        self._randomize_availability()
        return StepResult(observation=self._build_observation(), reward=0.0, done=False)

    async def close(self) -> None:
        self.current_task = None
        self.step_count = 0
        self.episode_rewards = []
        for farmer in self.farmers:
            farmer.available = True

    def state(self) -> dict:
        return {
            "current_job": self.current_task,
            "step": self.step_count,
            "max_steps": self.max_steps,
            "episode_rewards": self.episode_rewards,
            "farmers": [
                {
                    "name": f.name,
                    "skill": f.skill,
                    "experience": f.experience,
                    "available": f.available,
                }
                for f in self.farmers
            ],
        }

    async def step(self, action: AgroBridgeAction) -> StepResult:
        self.step_count += 1
        message = action.message.lower()

        selected_farmer = None
        for farmer in self.farmers:
            if farmer.name.lower() in message and farmer.available:
                selected_farmer = farmer
                break

        if selected_farmer is None:
            for farmer in self.farmers:
                if farmer.skill.lower() in message and farmer.available:
                    selected_farmer = farmer
                    break

        if selected_farmer is None:
            available = [f for f in self.farmers if f.available]
            selected_farmer = random.choice(available) if available else self.farmers[0]

        reward = grade_assignment(
            farmer_skill=selected_farmer.skill,
            farmer_experience=selected_farmer.experience,
            required_skill=self.current_task["required_skill"],
            difficulty=self.current_task["difficulty"],
            urgency=self.current_task["urgency"],
        )

        selected_farmer.available = False
        self.episode_rewards.append(reward)
        done = self.step_count >= self.max_steps or reward >= 1.0

        if done:
            obs = (
                f"Episode complete. Assigned {selected_farmer.name} "
                f"(skill:{selected_farmer.skill}, level:{selected_farmer.experience}) "
                f"to '{self.current_task['job']}'. "
                f"Final reward: {reward:.2f}. "
                f"Total episode rewards: {[round(r,2) for r in self.episode_rewards]}."
            )
        else:
            obs = (
                f"Assigned {selected_farmer.name} "
                f"(skill:{selected_farmer.skill}, level:{selected_farmer.experience}) "
                f"— reward: {reward:.2f}. Not optimal. "
                f"Step {self.step_count}/{self.max_steps}. "
                + self._build_observation()
            )

        return StepResult(observation=obs, reward=reward, done=done)