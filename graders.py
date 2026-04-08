def grade_easy(farmer_skill: str, required_skill: str) -> float:
    if farmer_skill == required_skill:
        return 0.95
    skill_groups = {
        "crop": {"cotton", "rice"},
        "field_ops": {"spraying", "tractor"},
        "resource": {"water"},
    }
    farmer_group = next((g for g, s in skill_groups.items() if farmer_skill in s), "none_a")
    required_group = next((g for g, s in skill_groups.items() if required_skill in s), "none_b")
    if farmer_group == required_group:
        return 0.45
    return 0.05


def grade_medium(farmer_skill: str, required_skill: str, difficulty: str = "medium") -> float:
    if farmer_skill == required_skill:
        return 0.9
    skill_groups = {
        "crop": {"cotton", "rice"},
        "field_ops": {"spraying", "tractor"},
        "resource": {"water"},
    }
    farmer_group = next((g for g, s in skill_groups.items() if farmer_skill in s), "none_a")
    required_group = next((g for g, s in skill_groups.items() if required_skill in s), "none_b")
    if farmer_group == required_group:
        return 0.5
    return 0.1


def grade_hard(farmer_skill: str, required_skill: str, difficulty: str = "hard") -> float:
    if farmer_skill == required_skill:
        return 0.85
    skill_groups = {
        "crop": {"cotton", "rice"},
        "field_ops": {"spraying", "tractor"},
        "resource": {"water"},
    }
    farmer_group = next((g for g, s in skill_groups.items() if farmer_skill in s), "none_a")
    required_group = next((g for g, s in skill_groups.items() if required_skill in s), "none_b")
    if farmer_group == required_group:
        return 0.3
    return 0.1
