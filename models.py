from pydantic import BaseModel


class Farmer:
    def __init__(self, name: str, skill: str, experience: str = "junior", available: bool = True):
        self.name = name
        self.skill = skill
        self.experience = experience
        self.available = available


class AgroBridgeAction(BaseModel):
    message: str


class StepResult(BaseModel):
    observation: str
    reward: float
    done: bool