from app.services.llm_service import call_llm


def analyze(topic, papers):
    print("🤖 Analyzer Agent working...")

    if not papers:
        return "No papers available for analysis."

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:200]}"
        for p in papers
    ])[:2000]

    prompt = f"""
You are a research analyst.

Topic: {topic}

Return output STRICTLY in this format:

Key Patterns:
- ...
- ...

Trends:
- ...
- ...

Agreements vs Disagreements:
- ...

Rules:
- Use bullet points
- Max 5 points per section
- No extra text outside sections

Papers:
{content}
"""

    try:
        result = call_llm(prompt)

        if not result or len(result.strip()) < 20:
            return "Analysis not available"

        # 🔥 STRUCTURE CHECK
        if "Key Patterns" not in result:
            print("⚠️ Analyzer format issue → fixing fallback")

            return f"""
Key Patterns:
- Patterns could not be clearly extracted

Trends:
- Trends not clearly identified

Agreements vs Disagreements:
- Mixed or unclear findings
"""

        return result.strip()

    except Exception as e:
        print("⚠️ Analyzer error:", str(e))
        return "Analysis temporarily unavailable"