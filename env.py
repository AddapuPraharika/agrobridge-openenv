import random
from tasks import tasks
from models import Farmer, StepResult, AgroBridgeObservation
from graders import grade_assignment

MAX_STEPS = 3


class AgroBridgeEnv:

    def __init__(self):
        self.farmers = [
            Farmer("Ramesh", "cotton"),
            Farmer("Suresh", "rice"),
            Farmer("Mahesh", "spraying")
        ]
        self.current_task = None

    async def reset(self):
        self.current_task = random.choice(tasks)
        obs = AgroBridgeObservation(
            echoed_message=f"Task reset: {self.current_task['job']}"
        )
        return StepResult(observation=obs, reward=0.0, done=False)

    def state(self):
        return {
            "current_job": self.current_task,
            "farmers": [
                {"name": farmer.name, "skill": farmer.skill}
                for farmer in self.farmers
            ]
        }

    async def step(self, action):
        try:
            farmer_index = int(action.message)
        except (ValueError, TypeError):
            farmer_index = 0

        farmer_index = max(0, min(farmer_index, len(self.farmers) - 1))
        selected_farmer = self.farmers[farmer_index]

        reward = grade_assignment(
            selected_farmer.skill,
            self.current_task["required_skill"],
            self.current_task["difficulty"]
        )

        obs = AgroBridgeObservation(
            echoed_message=f"Assigned {selected_farmer.name} to {self.current_task['job']}"
        )
        return StepResult(observation=obs, reward=reward, done=True)

    async def close(self):
        """Clean up environment resources. Required by the OpenEnv validator."""
        pass
