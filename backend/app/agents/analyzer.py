from app.services.llm_service import call_llm


def analyze(topic, papers):
    print("🤖 Analyzer Agent working...")

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:200]}"
        for p in papers
    ])

    prompt = f"""
You are a research analyst.

Topic: {topic}

Find:
- Key patterns
- Trends across papers
- Agreements vs disagreements

Papers:
{content}
"""

    try:
        return call_llm(prompt)
    except Exception as e:
        return f"Analysis error: {str(e)}"