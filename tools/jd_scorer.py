from utils.gemini import ask_llm

def jd_scorer(profile_data):

    prompt = f"""
Evaluate candidate for Python backend role.

Data:
{profile_data}

Rules:
- Strong Python/backend → 70–90
- FastAPI/PostgreSQL → 80+
- No data → 50
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
Recommendation: <Interview / Reject / Need Info>
"""

    result = ask_llm(prompt)

    if result:
        return result

    text = profile_data.lower()

    if "unknown" in text:
        return "Score: 50\nStrengths: Basic\nGaps: No data\nRecommendation: Need Info"

    if "civil" in text or "mechanical" in text:
        return "Score: 25\nStrengths: General\nGaps: No backend\nRecommendation: Reject"

    if "fastapi" in text or "postgresql" in text:
        return "Score: 85\nStrengths: FastAPI\nGaps: Cloud\nRecommendation: Interview"

    if "python" in text:
        return "Score: 75\nStrengths: Python\nGaps: Cloud\nRecommendation: Interview"

    return "Score: 50\nStrengths: Basic\nGaps: Missing\nRecommendation: Need Info"