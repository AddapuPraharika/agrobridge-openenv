def grade_crop(answer, expected=None):

    answer = str(answer).lower()

    if "rice" in answer or "wheat" in answer:
        return 0.9
    else:
        return 0.3


def grade_soil(answer, expected=None):

    answer = str(answer).lower()

    if "nitrogen" in answer or "phosphorus" in answer:
        return 0.85
    else:
        return 0.25


def grade_fertilizer(answer, expected=None):

    answer = str(answer).lower()

    if "organic" in answer or "urea" in answer:
        return 0.8
    else:
        return 0.2
