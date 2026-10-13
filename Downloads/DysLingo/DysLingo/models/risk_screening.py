def score_screening(answers):
    """
    Demonstration questionnaire score, not a clinically validated instrument.
    Each response is 0 (never), 1 (sometimes), or 2 (often).
    """
    keys = ["q1", "q2", "q3", "q4", "q5", "q6"]
    score = sum(max(0, min(2, int(answers.get(k, 0)))) for k in keys)
    if score <= 3:
        band = "Few reported difficulties"
        advice = "Continue supportive reading practice and monitor progress."
    elif score <= 7:
        band = "Some reported difficulties"
        advice = "Try accessible reading supports and discuss persistent concerns with the learner's teacher."
    else:
        band = "Several reported difficulties"
        advice = "Consider discussing reading concerns with a qualified educational or clinical professional."
    return {"score": score, "max_score": 12, "band": band, "advice": advice,
            "notice": "This informal demo questionnaire is not validated and cannot diagnose dyslexia."}
