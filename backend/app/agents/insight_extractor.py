import json
from app.services.llm_service import call_llm

def extract_insights(abstract: str):

    prompt = f"""
Return ONLY valid JSON. No explanation.

Format:
{{
  "points": ["...", "..."],
  "keywords": ["...", "..."],
  "why": "..."
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

        # 🔥 Try parsing JSON
        data = json.loads(response)

        # ✅ Validate structure
        return {
            "points": data.get("points", [])[:6],
            "keywords": data.get("keywords", [])[:10],
            "why": data.get("why", "Not available")
        }

    except Exception as e:
        print("⚠️ Insight extraction failed:", str(e))

        # 🔁 Safe fallback (VERY IMPORTANT)
        return {
            "points": [],
            "keywords": [],
            "why": "Could not extract insights"
        }