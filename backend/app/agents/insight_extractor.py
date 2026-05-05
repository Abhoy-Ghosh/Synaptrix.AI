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
Return ONLY valid JSON. No explanation. No text outside JSON.

Format:
{{
  "points": ["point1", "point2"],
  "keywords": ["k1", "k2"],
  "why": "one sentence"
}}

Rules:
- Points: 5-6 bullets, short and clear
- Keywords: 5-10 relevant terms
- Why: 1 simple sentence

Abstract:
{abstract}
"""

    # -----------------------------
    # RETRY LOOP (CRITICAL)
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
    # PARSE JSON (SAFE)
    # -----------------------------
    try:
        data = json.loads(response)

    except:
        # try extracting JSON block
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