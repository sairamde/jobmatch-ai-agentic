from utils.gemini import ask_llm


def clean_recommendation(text):
    text = text.lower()
    if "reject" in text:
        return "Reject"
    elif "interview" in text:
        return "Interview"
    elif "resume" in text:
        return "Request Resume"
    else:
        return "Need Info"


def jd_scorer(profile_data):

    text = profile_data.lower()

    # ❌ WRONG DOMAIN
    if any(x in text for x in ["civil", "mechanical", "accountant", "teacher"]):
        return """Score: 20
Strengths:
1. General academic background
Gaps:
1. Not relevant to backend role
Recommendation: Reject"""

    # ❌ NO DATA
    if not profile_data or len(profile_data) < 30:
        return """Score: 45
Strengths:
1. Limited information available
Gaps:
1. No sufficient profile data
Recommendation: Request Resume"""

    prompt = f"""
Evaluate candidate for Python backend role.

Data:
{profile_data}

Return STRICT format:

Score: <number>
Strengths:
1.
2.
3.
Gaps:
1.
2.
Recommendation:
"""

    result = ask_llm(prompt)

    # ✅ Gemini success
    if result:
        rec = clean_recommendation(result)

        if "Recommendation" in result:
            result = result.split("Recommendation")[0]

        return result.strip() + f"\nRecommendation: {rec}"

    # ✅ FALLBACK
    if "fastapi" in text or "postgresql" in text:
        return """Score: 85
Strengths:
1. FastAPI expertise
2. Strong backend development
3. Database handling skills
Gaps:
1. Limited cloud exposure
Recommendation: Interview"""

    if "python" in text:
        return """Score: 75
Strengths:
1. Strong Python knowledge
2. Backend development skills
3. API development experience
Gaps:
1. Limited cloud experience
2. No advanced architecture mentioned
Recommendation: Interview"""

    return """Score: 50
Strengths:
1. Basic knowledge
Gaps:
1. Missing data
Recommendation: Need Info"""