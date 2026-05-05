import json
from app.services.llm_service import call_llm


def extract_insights(abstract: str):

    # 🔒 Guard clause
    if not abstract or len(abstract) < 50:
        return {
            "points": [],
            "keywords": [],
            "why": "Insufficient abstract"
        }

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

    try:
        response = call_llm(prompt)

        if not response:
            raise ValueError("Empty LLM response")

        response = response.strip()

        # -----------------------------
        # STEP 1: Try direct JSON parse
        # -----------------------------
        try:
            data = json.loads(response)

        # -----------------------------
        # STEP 2: Extract JSON block
        # -----------------------------
        except:
            start = response.find("{")
            end = response.rfind("}") + 1

            if start == -1 or end == -1:
                raise ValueError("No JSON found")

            json_str = response[start:end]
            data = json.loads(json_str)

        # -----------------------------
        # STEP 3: Normalize fields
        # -----------------------------
        points = data.get("points") or data.get("bullet_points") or []
        keywords = data.get("keywords") or data.get("tags") or []
        why = data.get("why") or data.get("importance") or ""

        # -----------------------------
        # STEP 4: Force correct types
        # -----------------------------
        if not isinstance(points, list):
            points = [str(points)]

        if not isinstance(keywords, list):
            keywords = [str(keywords)]

        if not isinstance(why, str):
            why = str(why)

        return {
            "points": points[:6],
            "keywords": keywords[:10],
            "why": why if why else "Not available"
        }

    except Exception as e:
        print("⚠️ Insight extraction failed:", str(e))

        return {
            "points": [],
            "keywords": [],
            "why": "Could not extract insights"
        }