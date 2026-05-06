import json
from app.services.llm_service import call_llm


def extract_insights(abstract: str):

    # -----------------------------
    # GUARD CLAUSE
    # -----------------------------
    if not abstract or len(abstract) < 50:
        return {
            "points": [],
            "keywords": [],
            "why": "Insufficient abstract"
        }

    # -----------------------------
    # PROMPT
    # -----------------------------
    prompt = f"""
You are an elite AI Research Insight Extraction Engine.

Your task is to extract ONLY research-grounded insights from the provided abstract.

STRICT RULES:
- Return ONLY valid JSON
- No markdown
- No explanation
- No text outside JSON
- ONLY use information from the abstract
- Do NOT hallucinate missing details
- Do NOT introduce unrelated domains
- Avoid generic AI statements
- Keep outputs concise and technical
- Focus on methodologies, findings, contributions, limitations, or strategic relevance
- Keywords must be directly relevant to the abstract
- If information is weak, keep outputs minimal

OUTPUT FORMAT:
{{
  "points": [
    "short technical insight",
    "short technical insight"
  ],
  "keywords": [
    "keyword1",
    "keyword2"
  ],
  "why": "one concise sentence explaining research importance"
}}

QUALITY EXAMPLES:

GOOD POINT:
"Paper discusses ethical oversight in autonomous AI systems"

BAD POINT:
"AI is changing the future"

GOOD KEYWORD:
"cognitive warfare"

BAD KEYWORD:
"technology"

GOOD WHY:
"This research highlights challenges in maintaining human control over AI-driven decision systems."

BAD WHY:
"This paper is very useful."

RULES:
- points: 4-6 concise insights
- keywords: 5-10 technical terms
- why: exactly 1 sentence
- Do not repeat the same idea
- Avoid filler words

ABSTRACT:
{abstract}
"""

    # -----------------------------
    # RETRY LOOP
    # -----------------------------
    response = None

    for _ in range(2):
        try:
            response = call_llm(prompt)

            if (
                response
                and len(response.strip()) > 10
                and "temporarily unavailable" not in response.lower()
            ):
                break

        except Exception as e:
            print("⚠️ LLM call failed:", str(e))

    # -----------------------------
    # FINAL CHECK BEFORE PARSE
    # -----------------------------
    if not response or len(response.strip()) < 10:
        return {
            "points": [abstract[:120] + "..."],
            "keywords": [],
            "why": "Fallback extraction"
        }

    response = response.strip()

    # -----------------------------
    # SAFE JSON PARSE
    # -----------------------------
    try:
        data = json.loads(response)

    except:
        # Try extracting JSON block
        start = response.find("{")
        end = response.rfind("}") + 1

        if start == -1 or end == -1:
            return {
                "points": [abstract[:120] + "..."],
                "keywords": [],
                "why": "Fallback extraction"
            }

        try:
            json_str = response[start:end]
            data = json.loads(json_str)

        except:
            return {
                "points": [abstract[:120] + "..."],
                "keywords": [],
                "why": "Fallback extraction"
            }

    # -----------------------------
    # NORMALIZE FIELDS
    # -----------------------------
    points = data.get("points") or data.get("bullet_points") or []
    keywords = data.get("keywords") or data.get("tags") or []
    why = data.get("why") or data.get("importance") or ""

    # -----------------------------
    # FORCE TYPES
    # -----------------------------
    if not isinstance(points, list):
        points = [str(points)]

    if not isinstance(keywords, list):
        keywords = [str(keywords)]

    if not isinstance(why, str):
        why = str(why)

    # -----------------------------
    # FINAL CLEANUP
    # -----------------------------
    points = [p.strip() for p in points if p][:6]
    keywords = [k.strip() for k in keywords if k][:10]
    why = why.strip() if why else "Not available"

    # -----------------------------
    # FINAL RETURN
    # -----------------------------
    return {
        "points": points if points else [abstract[:120] + "..."],
        "keywords": keywords,
        "why": why
    }