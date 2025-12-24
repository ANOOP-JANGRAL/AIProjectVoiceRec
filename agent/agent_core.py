from agent.planner import plan
from agent.executor import execute
from agent.evaluator import evaluate
from agent.memory import Memory
from fuzzywuzzy import fuzz

memory = Memory()

# ----------------------------------------------------
# HINDI NUMBER DICTIONARY
# ----------------------------------------------------
hindi_numbers = {
    "एक": 1, "दो": 2, "तीन": 3, "चार": 4, "पांच": 5, "पाँच": 5, "छह": 6,
    "सात": 7, "आठ": 8, "नौ": 9, "दस": 10, "ग्यारह": 11, "बारह": 12,
    "तेरह": 13, "चौदह": 14, "पंद्रह": 15, "सोलह": 16, "सत्रह": 17,
    "अठारह": 18, "उन्नीस": 19, "बीस": 20,

    "इक्कीस": 21, "बाईस": 22, "तेईस": 23, "चौबीस": 24, "पच्चीस": 25,
    "छब्बीस": 26, "सत्ताईस": 27, "अट्ठाईस": 28, "उनतीस": 29, "तीस": 30,

    "इकतीस": 31, "बत्तीस": 32, "तैंतीस": 33, "चौंतीस": 34, "पैंतीस": 35,
    "छत्तीस": 36, "सैंतीस": 37, "अड़तीस": 38, "उनतालीस": 39, "चालीस": 40,

    "इकतालीस": 41, "बयालिस": 42, "तैंतालीस": 43, "चवालीस": 44, "पैंतालीस": 45,
    "छियालिस": 46, "सैंतालीस": 47, "अड़तालीस": 48, "उनचास": 49, "पचास": 50,

    "इक्यावन": 51, "बावन": 52, "तिरेपन": 53, "चौवन": 54, "पचपन": 55,
    "छप्पन": 56, "सत्तावन": 57, "अट्ठावन": 58, "उनसठ": 59, "साठ": 60,

    "इकसठ": 61, "बासठ": 62, "तिरसठ": 63, "चौंसठ": 64, "पैंसठ": 65,
    "छियासठ": 66, "सड़सठ": 67, "अड़सठ": 68, "उनहत्तर": 69, "सत्तर": 70,

    "इकहत्तर": 71, "बहत्तर": 72, "तिहत्तर": 73, "चौहत्तर": 74, "पचहत्तर": 75,
    "छिहत्तर": 76, "सतहत्तर": 77, "अठहत्तर": 78, "उन्यासी": 79, "अस्सी": 80,

    "इक्यासी": 81, "बयासी": 82, "तिरासी": 83, "चौरासी": 84, "पचासी": 85,
    "छियासी": 86, "सत्तासी": 87, "अठासी": 88, "नवासी": 89, "नब्बे": 90,

    "इक्यानबे": 91, "बानवे": 92, "तिरानबे": 93, "चौरानबे": 94, "पंचानबे": 95,
    "छियानबे": 96, "सत्तानबे": 97, "अट्ठानबे": 98, "निन्यानबे": 99, "सौ": 100
}


# ----------------------------------------------------
# EXTRACT HINDI NUMBER (FUZZY)
# ----------------------------------------------------
def extract_hindi_number(text):
    digits = "".join(c for c in text if c.isdigit())
    if digits:
        return int(digits)

    words = text.split()
    best = None
    best_score = 0

    for w in words:
        for hn in hindi_numbers:
            score = fuzz.ratio(w, hn)
            if score > best_score and score >= 65:
                best = hn
                best_score = score

    return hindi_numbers[best] if best else None

# ----------------------------------------------------
# INCOME EXTRACTOR (supports लाख/हजार/सौ)
# ----------------------------------------------------
def extract_income(text):
    num = extract_hindi_number(text)

    if num is None:
        return None

    if "लाख" in text:
        return num * 100000
    if "हजार" in text or "हज़ार" in text:
        return num * 1000
    if "सौ" in text:
        return num * 100

    return num

# ----------------------------------------------------
# CASTE EXTRACTOR WITH OPTIONS
# ----------------------------------------------------
def extract_caste(text):
    t = text.lower()

    # numeric selection
    if "1" in t: return "SC"
    if "2" in t: return "ST"
    if "3" in t: return "OBC"
    if "4" in t: return "GENERAL"

    # word-based selection
    if "sc" in t or "एससी" in t: return "SC"
    if "st" in t or "एसटी" in t: return "ST"
    if "obc" in t or "ओबीसी" in t: return "OBC"
    if "general" in t or "जनरल" in t or "सामान्य" in t: return "GENERAL"

    return None

# ----------------------------------------------------
# MAIN AGENT LOGIC
# ----------------------------------------------------
def agent_step(text):
    intent = plan(text)

    # UNKNOWN
    if intent == "UNKNOWN":
        return "मैं आपकी बात नहीं समझ पाया, कृपया दोबारा बोलें।"

    # NAME
    if intent == "USER_NAME":
        memory.remember("name", text)
        return "अच्छा लगा आपका नाम जानकर! कृपया अपनी उम्र बताएं।"

    # CLASS
    if intent == "USER_CLASS":
        memory.remember("class", text)
        return "ठीक है! कृपया अपनी उम्र बताएं।"

    # AGE
    if intent == "ASK_AGE":
        age = extract_hindi_number(text)
        if age:
            memory.remember("age", age)
            return f"ठीक है, आपकी उम्र {age} दर्ज कर ली गई है। अब अपनी मासिक आय बताएं।"
        return "कृपया अपनी उम्र बताएं।"

    # INCOME
    if intent == "ASK_INCOME":
        income = extract_income(text)
        if income:
            memory.remember("income", income)
            return (
                f"ठीक है, आपकी मासिक आय {income} रुपये दर्ज कर ली गई है।\n"
                "अब अपनी जाति चुनें:\n1. SC\n2. ST\n3. OBC\n4. General"
            )
        return "कृपया अपनी मासिक आय बताएं।"

    # CASTE
    if intent == "ASK_CASTE":
        caste = extract_caste(text)

        if caste is None:
            return "कृपया अपनी जाति चुनें:\n1. SC\n2. ST\n3. OBC\n4. General"

        memory.remember("caste", caste)

        #  NOW CHECK ELIGIBILITY IMMEDIATELY
        result = execute("CHECK_ELIGIBILITY", memory)
        return result

    # CHECK ELIGIBILITY (if user asks directly)
    if intent == "CHECK_ELIGIBILITY":

        if memory.get("age") is None:
            return "कृपया अपनी उम्र बताएं।"

        if memory.get("income") is None:
            return "कृपया अपनी मासिक आय बताएं।"

        if memory.get("caste") is None:
            return "कृपया अपनी जाति चुनें:\n1. SC\n2. ST\n3. OBC\n4. General"

        result = execute("CHECK_ELIGIBILITY", memory)

        if not result:
            return "❌ आप किसी भी योजना के लिए पात्र नहीं हैं।"

        return f"आप निम्नलिखित योजनाओं के लिए पात्र हैं:\n{result}"

    return "त्रुटि हुई।"
