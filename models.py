from pydantic import BaseModel


class Farmer:
    def __init__(self, name: str, skill: str):
        self.name = name
        self.skill = skill


class AgroBridgeAction(BaseModel):
    message: str = "0"


class AgroBridgeObservation:
    def __init__(self, echoed_message: str):
        self.echoed_message = echoed_message


class StepResult:
    def __init__(self, observation, reward: float, done: bool):
        self.observation = observation
        self.reward = reward
        self.done = done
