from typing import Literal

SKILL_GROUPS: dict[str, set[str]] = {
    "crop":      {"cotton", "rice"},
    "field_ops": {"spraying", "tractor"},
    "resource":  {"water"},
}

EXPERIENCE_BONUS: dict[str, dict[str, float]] = {
    "easy":   {"senior": 0.0,  "junior": 0.0},
    "medium": {"senior": 0.1,  "junior": -0.1},
    "hard":   {"senior": 0.2,  "junior": -0.2},
}

URGENCY_MULTIPLIER: dict[int, float] = {
    1: 1.0,
    2: 1.1,
    3: 1.2,
}


def get_skill_group(skill: str | None) -> str | None:
    """Return the skill group name for a given skill, or None if not found."""
    if skill is None:
        return None
    for group, skills in SKILL_GROUPS.items():
        if skill in skills:
            return group
    return None


def grade_assignment(
    farmer_skill: str,
    farmer_experience: str,
    required_skill: str,
    difficulty: str,
    urgency: int,
) -> float:
    """
    Compute the reward for assigning a farmer to a task.

    Formula:
        final_reward = clamp(0, 1, (base_reward + experience_bonus) * urgency_multiplier)

    Base reward:
        1.0  — exact skill match
        0.5  — same skill group (partial match)
        0.0  — no match

    Experience bonus (applied by difficulty):
        easy:   senior +0.0,  junior +0.0
        medium: senior +0.1,  junior -0.1
        hard:   senior +0.2,  junior -0.2

    Urgency multiplier:
        LOW (1): ×1.0 | MEDIUM (2): ×1.1 | HIGH (3): ×1.2
    """
    if farmer_skill == required_skill:
        base_reward = 1.0
    else:
        farmer_group = get_skill_group(farmer_skill)
        required_group = get_skill_group(required_skill)
        if farmer_group is not None and farmer_group == required_group:
            base_reward = 0.5
        else:
            base_reward = 0.0

    bonus = EXPERIENCE_BONUS.get(difficulty, {}).get(farmer_experience, 0.0)
    multiplier = URGENCY_MULTIPLIER.get(urgency, 1.0)

    final = (base_reward + bonus) * multiplier
    return round(max(0.0, min(1.0, final)), 2)