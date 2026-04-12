def grade_assignment(farmer_skill, required_skill, difficulty="medium"):
    """
    Returns a score strictly between 0 and 1 (never 0.0 or 1.0).
    Each difficulty band maps to a distinct partial-credit range.
    """
    if farmer_skill == required_skill:
        if difficulty == "easy":
            return 0.95
        elif difficulty == "medium":
            return 0.85
        else:  # hard
            return 0.75

    elif farmer_skill in ["cotton", "rice"] and required_skill in ["cotton", "rice"]:
        # Related crop skills — decent partial credit
        if difficulty == "easy":
            return 0.65
        elif difficulty == "medium":
            return 0.55
        else:
            return 0.45

    elif farmer_skill in ["cotton", "rice"]:
        # Some transferable skill
        if difficulty == "easy":
            return 0.35
        elif difficulty == "medium":
            return 0.25
        else:
            return 0.15

    else:
        # Unrelated skill — minimal but non-zero credit
        if difficulty == "easy":
            return 0.12
        elif difficulty == "medium":
            return 0.08
        else:
            return 0.05
