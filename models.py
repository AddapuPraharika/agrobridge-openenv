class Farmer:
    def __init__(self, name: str, skill: str, experience: str = "junior", available: bool = True):
        self.name = name
        self.skill = skill
        self.experience = experience
        self.available = available


class AgroBridgeAction:
    def __init__(self, message: str):
        self.message = message


class StepResult:
    def __init__(self, observation: str, reward: float, done: bool):
        self.observation = observation
        self.reward = reward
        self.done = done
