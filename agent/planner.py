def plan(t):
    t = t.lower()

    # New: Detect name introductions
    if "मेरा नाम" in t or "मेरी नाम" in t:
        return "USER_NAME"

    # New: Detect class/grade
    if "कक्षा" in t or "क्लास" in t:
        return "USER_CLASS"

    # Existing logic
    if "आय" in t or "इनकम" in t:
        return "ASK_INCOME"

    if "उम्र" in t or "age" in t:
        return "ASK_AGE"

    if "जाति" in t or "caste" in t:
        return "ASK_CASTE"

    if "योजना" in t or "scheme" in t:
        return "CHECK_ELIGIBILITY"

    return "UNKNOWN"
