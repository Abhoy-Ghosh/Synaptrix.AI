from app.services.llm_service import call_llm


def analyze(topic, papers):
    print("🤖 Analyzer Agent working...")

    if not papers:
        return "No papers available for analysis."

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:200]}"
        for p in papers
    ])[:2000]  # 🔥 limit size

    prompt = f"""
You are a research analyst.

Topic: {topic}

Analyze the papers and give output in this format:

Key Patterns:
- ...
- ...

Trends:
- ...
- ...

Agreements vs Disagreements:
- ...

Rules:
- Keep it concise
- Use bullet points
- Max 5 points per section

Papers:
{content}
"""

    try:
        result = call_llm(prompt)

        # 🔥 basic validation
        if not result or len(result.strip()) < 20:
            return "Analysis not available"

        return result

    except Exception as e:
        print("⚠️ Analyzer error:", str(e))
        return "Analysis temporarily unavailable"