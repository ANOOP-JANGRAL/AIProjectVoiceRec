from tools.eligibility_engine import check_eligibility
from tools.scheme_retriever import search_scheme

def execute(action, memory):

    if action == "CHECK_ELIGIBILITY":
        age = memory.get("age")
        income = memory.get("income")
        caste = memory.get("caste")

        # Missing fields
        if age is None:
            return "कृपया अपनी उम्र बताएं।"

        if income is None:
            return "कृपया अपनी मासिक आय बताएं।"

        if caste is None:
            return (
                "कृपया अपनी जाति चुनें:\n"
                "1. SC\n"
                "2. ST\n"
                "3. OBC\n"
                "4. General"
            )

        # Compute eligibility
        schemes = check_eligibility(memory.data)

        # No schemes found
        if not schemes:
            return "❌ आप किसी भी योजना के लिए पात्र नहीं हैं।"

        # Build final text
        final_text = "आप निम्नलिखित योजनाओं के लिए पात्र हैं:\n\n"

        for s in schemes:
            desc = search_scheme(s)
            final_text += f"✔ {s} – {desc}\n"

        return final_text

    return None
