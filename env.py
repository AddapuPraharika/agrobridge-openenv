import random
from tasks import tasks
from models import Farmer, AgroBridgeAction, StepResult


class AgroBridgeEnv:

    def __init__(self):
        self.farmers = [
            Farmer("Ramesh", "cotton"),
            Farmer("Suresh", "rice"),
            Farmer("Mahesh", "spraying"),
            Farmer("Dinesh", "tractor"),
            Farmer("Naresh", "water"),
        ]
        self.current_task = None

    async def reset(self):
        self.current_task = random.choice(tasks)
        obs = (
            f"Job: {self.current_task['job']}. "
            f"Required skill: {self.current_task['required_skill']}. "
            f"Difficulty: {self.current_task['difficulty']}. "
            f"Available farmers: "
            + ", ".join(f"{f.name} ({f.skill})" for f in self.farmers)
        )
        return StepResult(observation=obs, reward=0.0, done=False)

    def state(self):
        return {
            "current_job": self.current_task,
            "farmers": [
                {"name": farmer.name, "skill": farmer.skill}
                for farmer in self.farmers
            ],
        }

    async def step(self, action: AgroBridgeAction):
        message = action.message.lower()

        selected_farmer = None
        for farmer in self.farmers:
            if farmer.name.lower() in message or farmer.skill.lower() in message:
                selected_farmer = farmer
                break

        if selected_farmer is None:
            selected_farmer = random.choice(self.farmers)

        required_skill = self.current_task["required_skill"]
        reward = self._grade(selected_farmer.skill, required_skill)

        obs = (
            f"Assigned {selected_farmer.name} (skill: {selected_farmer.skill}) "
            f"to job '{self.current_task['job']}' "
            f"(required: {required_skill}). "
            f"Reward: {reward}"
        )

        return StepResult(observation=obs, reward=reward, done=True)

    def _grade(self, farmer_skill: str, required_skill: str) -> float:
        if farmer_skill == required_skill:
            return 1.0
        skill_groups = {
            "crop": {"cotton", "rice"},
            "field_ops": {"spraying", "tractor"},
            "resource": {"water"},
        }
        farmer_group = None
        required_group = None
        for group, skills in skill_groups.items():
            if farmer_skill in skills:
                farmer_group = group
            if required_skill in skills:
                required_group = group
        if farmer_group and farmer_group == required_group:
            return 0.5
        return 0.0
