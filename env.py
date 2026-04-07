import random
from tasks import tasks
from models import Farmer, AgroBridgeAction, StepResult
from graders import grade_assignment

MAX_STEPS = 3


class AgroBridgeEnv:
    """
    AgroBridge OpenEnv — multi-step RL environment for agricultural labor matching.

    The agent observes a job description with required skill, difficulty, and urgency,
    then assigns one of the available farmers. Rewards are computed by graders.py using
    skill match, experience level, and urgency multiplier.

    Episode structure:
    - reset()  → returns initial StepResult (done=False)
    - step()   → returns StepResult with reward; done=True when max steps reached
                 or a perfect reward (≥1.0) is achieved
    - close()  → resets state cleanly
    """

    def __init__(self) -> None:
        self.farmers: list[Farmer] = [
            Farmer("Ramesh",  "cotton",   experience="senior"),
            Farmer("Suresh",  "rice",     experience="junior"),
            Farmer("Mahesh",  "spraying", experience="senior"),
            Farmer("Dinesh",  "tractor",  experience="junior"),
            Farmer("Naresh",  "water",    experience="senior"),
            Farmer("Lokesh",  "cotton",   experience="junior"),
            Farmer("Ganesh",  "rice",     experience="senior"),
        ]
        self.current_task: dict | None = None
        self.step_count: int = 0
        self.max_steps: int = MAX_STEPS
        self.episode_rewards: list[float] = []

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _randomize_availability(self) -> None:
        for farmer in self.farmers:
            farmer.available = random.random() > 0.3
        if not any(f.available for f in self.farmers):
            self.farmers[0].available = True

    def _available_farmers(self) -> list[Farmer]:
        return [f for f in self.farmers if f.available]

    def _build_observation(self) -> str:
        available = self._available_farmers()
        farmer_list = ", ".join(
            f"{f.name} (skill:{f.skill}, level:{f.experience})"
            for f in available
        )
        urgency_label = {1: "LOW", 2: "MEDIUM", 3: "HIGH"}.get(
            self.current_task["urgency"], "UNKNOWN"
        )
        return (
            f"Job: {self.current_task['job']}. "
            f"Description: {self.current_task['description']} "
            f"Required skill: {self.current_task['required_skill']}. "
            f"Difficulty: {self.current_task['difficulty']}. "
            f"Urgency: {urgency_label}. "
            f"Step: {self.step_count + 1}/{self.max_steps}. "
            f"Available farmers: {farmer_list}."
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def reset(self) -> StepResult:
        self.current_task = random.choice(tasks)
        self.step_count = 0
        self.episode_rewards = []
        for f in self.farmers:
            f.available = True
        self._randomize_availability()
        return StepResult(observation=self._build_observation(), reward=0.0, done=False)

    async def close(self) -> None:
        self.current_task = None
        self.step_count = 0
        self.episode_rewards = []
        for f in self.farmers:
            f.available = True

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
        available = self._available_farmers()


        if not available:
            return StepResult(
                observation=(
                    "No farmers are available. Episode ended early. "
                    f"Total episode rewards: {[round(r, 2) for r in self.episode_rewards]}."
                ),
                reward=0.0,
                done=True,
            )
        selected_farmer: Farmer | None = None

        for farmer in available:
            if farmer.name.lower() in message:
                selected_farmer = farmer
                break

        if selected_farmer is None:
            for farmer in available:
                if farmer.skill.lower() in message:
                    selected_farmer = farmer
                    break

        # --- If the agent's message is ambiguous, penalise without consuming a farmer ---
        if selected_farmer is None:
            if self.step_count >= self.max_steps:
                return StepResult(
                    observation=(
                        "Ambiguous action — no farmer name or skill found in message. "
                        "Episode ended. "
                        f"Total episode rewards: {[round(r, 2) for r in self.episode_rewards]}."
                    ),
                    reward=0.0,
                    done=True,
                )
            return StepResult(
                observation=(
                    "Ambiguous action — no farmer name or skill found in your message. "
                    "Please name a farmer explicitly. "
                    + self._build_observation()
                ),
                reward=0.0,
                done=False,
            )
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
                f"Total episode rewards: {[round(r, 2) for r in self.episode_rewards]}."
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