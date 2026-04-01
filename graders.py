def grade_assignment(farmer_skill, required_skill):

    if farmer_skill == required_skill:
        return 1.0

    elif farmer_skill in ["cotton", "rice"]:
        return 0.5

    else:
        return 0.0