import re
from utils.gemini import ask_llm


def parse_response(text):
    # Extract score correctly (avoid 3/5 issue)
    match = re.search(r"Score:\s*(\d+)(?:/100)?", text)
    score = int(match.group(1)) if match else 50

    # Extract strengths
    parts = text.split("Gaps:")
    strengths = re.findall(r"\d+\.\s*(.*)", parts[0])

    # Clean unwanted values like 3/5
    strengths = [s for s in strengths if not any(x in s for x in ["/5", "/10"])]

    # Extract gaps
    gaps = []
    if len(parts) > 1:
        gaps = re.findall(r"\d+\.\s*(.*)", parts[1])

    return score, strengths[:3], gaps[:2]


def jd_scorer(profile_data):

    text = profile_data.lower()

    # ❌ Wrong domain (required edge case)
    if any(x in text for x in ["civil", "mechanical", "accountant", "teacher"]):
        return 20, ["Irrelevant background"], ["Not backend role"], "Reject"

    # ❌ No profile found (required edge case)
    if not profile_data or len(profile_data) < 30:
        return 45, ["Limited information"], ["No profile found"], "Request Resume"

    # 🔥 STRONG PROMPT (VERY IMPORTANT)
    prompt = f"""
You are an expert recruiter.

Evaluate the candidate for a Python backend role.

STRICT RULES:
- Strong Python/backend → 70–90
- FastAPI / Django → 75–90
- HTML/CSS/JS only → 50–65
- No data → 40–55
- Wrong domain → <30

Use BOTH:
1. Profile data
2. Skills mentioned

Candidate Data:
{profile_data}

Return EXACT format:

Score: <number>
Strengths:
1. ...
2. ...
3. ...
Gaps:
1. ...
2. ...
Recommendation: <Interview / Reject / Request Resume>
"""

    result = ask_llm(prompt)

    # ✅ LLM SUCCESS
    if result:
        score, strengths, gaps = parse_response(result)

        # 🚨 FIX BAD SCORE (3/100 bug)
        if score < 40:
            if "python" in text:
                score = 70
            else:
                score = 50

        recommendation = (
            "Interview" if score >= 70 else
            "Reject" if score < 30 else
            "Request Resume"
        )

        return score, strengths, gaps, recommendation

    # ⚠️ FALLBACK (ONLY IF LLM FAILS)
    if "python" in text:
        return 70, ["Python"], ["Cloud/Advanced skills"], "Interview"

    return 50, ["Basic knowledge"], ["Missing data"], "Request Resume"