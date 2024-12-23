

def create_feedback_text(destination, lang):
    feedback_text = lang.get("tips", {}).get(destination, "No tips available for this feedback type.")
    return feedback_text