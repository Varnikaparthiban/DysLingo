import re
from difflib import SequenceMatcher

def words(text):
    return re.findall(r"[^\W_]+(?:['’][^\W_]+)?", (text or "").lower(), flags=re.UNICODE)

def analyze_reading(target_text, spoken_text, duration_seconds=60):
    target = words(target_text)
    spoken = words(spoken_text)
    if not target:
        return {"accuracy": 0, "wpm": 0, "errors": 0, "pauses": 0, "duration_seconds": 0, "feedback": "Please provide a passage to analyze."}

    matcher = SequenceMatcher(a=target, b=spoken, autojunk=False)
    matching = sum(block.size for block in matcher.get_matching_blocks())
    accuracy = round(100 * matching / max(len(target), 1), 1)
    errors = max(len(target) - matching, 0) + max(len(spoken) - matching, 0)
    # Demo baseline: duration can be supplied by future timed capture; current form uses a 60-second estimate.
    duration_seconds = max(float(duration_seconds or 60), 1)
    wpm = round(len(spoken) / (duration_seconds / 60), 1)
    pauses = max((spoken_text or "").count("..."), (spoken_text or "").count("…"))
    if accuracy >= 90:
        feedback = "Strong match with the passage. Keep practicing at a comfortable pace."
    elif accuracy >= 70:
        feedback = "Good effort. Try shorter sections and listen to the passage before reading it again."
    else:
        feedback = "Try reading one sentence at a time, with audio support and more practice. This score is not a diagnosis."
    return {"accuracy": accuracy, "wpm": wpm, "errors": errors, "pauses": pauses, "duration_seconds": duration_seconds, "feedback": feedback}
