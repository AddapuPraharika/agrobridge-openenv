import random
from tasks import tasks
from models import Farmer
from graders import grade_assignment


class AgroBridgeEnv:

    def __init__(self):

        self.farmers = [
            Farmer("Ramesh", "cotton"),
            Farmer("Suresh", "rice"),
            Farmer("Mahesh", "spraying")
        ]

        self.current_task = None


    def reset(self):

        self.current_task = random.choice(tasks)

        return self.current_task


    def state(self):

        return {
            "current_job": self.current_task,
            "farmers": [
                {"name": farmer.name, "skill": farmer.skill}
                for farmer in self.farmers
            ]
        }


    def step(self, action):

        selected_farmer = self.farmers[action]

        reward = grade_assignment(
            selected_farmer.skill,
            self.current_task["required_skill"]
        )

        done = True

        return self.current_task, reward, done