def grade_easy(farmer_skill, required_skill):
    if farmer_skill == required_skill:
        return 0.95
    elif farmer_skill in ["cotton", "rice"]:
        return 0.4
    else:
        return 0.05

def grade_medium(farmer_skill, required_skill, difficulty):
    if farmer_skill == required_skill:
        return 0.9
    elif difficulty == "medium" and farmer_skill in ["cotton", "rice", "spraying"]:
        return 0.45
    else:
        return 0.1

def grade_hard(farmer_skill, required_skill, difficulty):
    if farmer_skill == required_skill and difficulty == "hard":
        return 0.85
    elif farmer_skill == required_skill:
        return 0.7
    elif difficulty == "hard":
        return 0.15
    else:
        return 0.1
