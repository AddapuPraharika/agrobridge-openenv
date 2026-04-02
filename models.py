# models.py

class Farmer:
def **init**(self, name: str, skill: str):
self.name = name
self.skill = skill

class AgroBridgeAction:
def **init**(self, message: str):
self.message = message

class AgroBridgeObservation:
def **init**(self, echoed_message: str):
self.echoed_message = echoed_message

class StepResult:
def **init**(self, observation, reward: float, done: bool):
self.observation = observation
self.reward = reward
self.done = done

