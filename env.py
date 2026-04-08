import random
from dataclasses import dataclass
from typing import Optional, Any
from tasks import tasks
from models import Farmer


@dataclass
class AgroBridgeAction:
    message: str


@dataclass
class StepResult:
    observation: Any
    reward: float
    done: bool
    info: dict = None


class AgroBridgeEnv:

    def __init__(self):
        self.farmers = [
            Farmer("Ramesh", "cotton"),
            Farmer("Suresh", "rice"),
            Farmer("Mahesh", "spraying"),
        ]
        self.current_task = None
        self.max_steps = 8
        self.steps_taken = 0

    @classmethod
    async def from_docker_image(cls, image_name: Optional[str] = None):
        return cls()

    async def reset(self) -> StepResult:
        self.current_task = random.choice(tasks)
        self.steps_taken = 0
        obs = {
            "job": self.current_task["job"],
            "required_skill": self.current_task["required_skill"],
            "difficulty": self.current_task["difficulty"],
            "farmers": [{"name": f.name, "skill": f.skill} for f in self.farmers],
        }
        return StepResult(observation=obs, reward=0.0, done=False)

    async def step(self, action: AgroBridgeAction) -> StepResult:
        self.steps_taken += 1

        # Parse farmer index from action message
        farmer_index = self._parse_action(action.message)
        selected_farmer = self.farmers[farmer_index % len(self.farmers)]

        grader = self.current_task["grader"]
        difficulty = self.current_task["difficulty"]

        # Call the right grader signature
        try:
            if difficulty == "easy":
                reward = grader(selected_farmer.skill, self.current_task["required_skill"])
            else:
                reward = grader(selected_farmer.skill, self.current_task["required_skill"], difficulty)
        except Exception:
            reward = 0.1

        # Clamp strictly within (0, 1) as a safety net
        reward = max(0.05, min(0.95, float(reward)))

        done = self.steps_taken >= self.max_steps

        obs = {
            "job": self.current_task["job"],
            "required_skill": self.current_task["required_skill"],
            "assigned_farmer": selected_farmer.name,
            "farmer_skill": selected_farmer.skill,
        }

        return StepResult(observation=obs, reward=reward, done=done)

    def _parse_action(self, message: str) -> int:
        msg = message.lower()
        for i, farmer in enumerate(self.farmers):
            if farmer.name.lower() in msg or farmer.skill.lower() in msg:
                return i
        # fallback: try to find a digit
        for ch in message:
            if ch.isdigit():
                return int(ch) % len(self.farmers)
        return random.randint(0, len(self.farmers) - 1)

    async def close(self):
        pass
