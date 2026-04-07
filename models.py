from pydantic import BaseModel, Field


class Farmer:
    """Represents an agricultural worker with a skill, experience level, and availability."""

    def __init__(
        self,
        name: str,
        skill: str,
        experience: str = "junior",
        available: bool = True,
    ) -> None:
        self.name = name
        self.skill = skill
        self.experience = experience
        self.available = available

    def __repr__(self) -> str:
        return (
            f"Farmer(name={self.name!r}, skill={self.skill!r}, "
            f"experience={self.experience!r}, available={self.available})"
        )

    def __str__(self) -> str:
        status = "available" if self.available else "unavailable"
        return f"{self.name} ({self.skill}, {self.experience}, {status})"


class AgroBridgeAction(BaseModel):
    """Action submitted by the agent — a natural language farmer assignment message."""

    message: str = Field(
        ...,
        description=(
            "Natural language message naming the farmer to assign and optionally explaining why. "
            "Example: 'Assign Mahesh because he is a senior spraying expert.'"
        ),
        min_length=1,
        max_length=500,
    )


class StepResult(BaseModel):
    """The result returned by reset() and step()."""

    observation: str = Field(..., description="Natural language description of the current state.")
    reward: float = Field(..., ge=0.0, le=1.0, description="Reward for this step [0.0, 1.0].")
    done: bool = Field(..., description="True if the episode has ended.")