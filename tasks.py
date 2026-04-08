from graders import grade_easy, grade_medium, grade_hard

tasks = [
    {
        "name": "easy",
        "job": "cotton harvesting",
        "required_skill": "cotton",
        "difficulty": "easy",
        "grader": grade_easy,
    },
    {
        "name": "medium",
        "job": "rice planting",
        "required_skill": "rice",
        "difficulty": "medium",
        "grader": grade_medium,
    },
    {
        "name": "hard",
        "job": "pesticide spraying",
        "required_skill": "spraying",
        "difficulty": "hard",
        "grader": grade_hard,
    },
    {
        "name": "medium",
        "job": "irrigation management",
        "required_skill": "water",
        "difficulty": "medium",
        "grader": grade_medium,
    },
    {
        "name": "hard",
        "job": "tractor ploughing",
        "required_skill": "tractor",
        "difficulty": "hard",
        "grader": grade_hard,
    },
]
