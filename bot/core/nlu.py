def infer_intent(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["voo", "passagem", "flight"]):
        return "flight"
    if any(w in t for w in ["hotel", "hosped"]):
        return "hotel"
    return "smalltalk"
