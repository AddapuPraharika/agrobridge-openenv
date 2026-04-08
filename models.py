class Farmer:
    def __init__(self, name: str, skill: str):
        self.name = name
        self.skill = skill


class AgroBridgeAction:
    def __init__(self, message: str):
        self.message = message


class StepResult:
    def __init__(self, observation, reward: float, done: bool):
        self.observation = observation
        self.reward = reward
        self.done = done
