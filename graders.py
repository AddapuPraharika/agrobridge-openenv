SKILL_GROUPS = {
    "crop": {"cotton", "rice"},
    "field_ops": {"spraying", "tractor"},
    "resource": {"water"},
}

EXPERIENCE_BONUS = {
    "easy":   {"senior": 0.0,  "junior": 0.0},
    "medium": {"senior": 0.1,  "junior": -0.1},
    "hard":   {"senior": 0.2,  "junior": -0.2},
}

URGENCY_MULTIPLIER = {1: 1.0, 2: 1.1, 3: 1.2}


def get_skill_group(skill: str):
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