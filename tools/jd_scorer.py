from utils.gemini import ask_llm

def jd_scorer(profile_data):

    text = profile_data.lower()

    # ❌ WRONG DOMAIN (Score <30)
    if any(x in text for x in ["civil", "mechanical", "accountant", "teacher"]):
        return """Score: 20
Strengths: General background
Gaps: Not relevant to backend role
Recommendation: Reject"""

    # ❌ NO PROFILE FOUND (Score 40–55)
    if not profile_data or len(profile_data) < 30:
        return """Score: 45
Strengths: Limited information
Gaps: No sufficient profile data
Recommendation: Request Resume"""

    prompt = f"""
Evaluate candidate for Python backend role.

IMPORTANT:
- Use skills mentioned in input data
- Follow strict rules

Data:
{profile_data}

Rules:
- Strong Python/backend → 70–90
- FastAPI/PostgreSQL → 80+
- No data → 40–55
- Wrong domain → below 30

Return format:

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

    if result:
        return result

    # ✅ FALLBACK
    if "fastapi" in text or "postgresql" in text:
        return """Score: 85
Strengths: FastAPI, Database
Gaps: Cloud
Recommendation: Interview"""

    if "python" in text:
        return """Score: 75
Strengths: Python
Gaps: Cloud
Recommendation: Interview"""

    return """Score: 50
Strengths: Basic knowledge
Gaps: Missing data
Recommendation: Need Info"""