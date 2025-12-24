def check_eligibility(d):
    age = d.get("age")
    income = d.get("income")
    caste = d.get("caste")

    res = []

    # 1. PM Ujjwala Yojana (poor families)
    if age and age >= 18 and income and income <= 200000:
        res.append("प्रधानमंत्री उज्ज्वला योजना")

    # 2. Old Age Pension
    if age and age >= 60:
        res.append("राष्ट्रीय वृद्धावस्था पेंशन योजना")

    # 3. SC/ST entrepreneurship support
    if caste in ["SC", "ST"]:
        res.append("दलित उद्यमिता विकास योजना")

    # 4. OBC scholarship (youth)
    if caste == "OBC" and age and age < 35:
        res.append("ओबीसी छात्रवृत्ति योजना")

    # 5. Skill development for all youth
    if age and 18 <= age <= 45:
        res.append("प्रधानमंत्री कौशल विकास योजना")

    # 6. Mudra loan scheme
    if age and 18 <= age <= 60 and income and income <= 1000000:
        res.append("मुद्रा लोन योजना")

    return res
