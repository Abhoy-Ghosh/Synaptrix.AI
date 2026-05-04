from app.services.llm_service import call_llm


def find_gaps(topic, papers):
    print("🤖 Gap Finder Agent working...")

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:200]}"
        for p in papers
    ])

    prompt = f"""
You are a research strategist.

Topic: {topic}

Find:
- Missing research areas
- Under-explored topics
- Future directions (based on missing coverage)

Papers:
{content}
"""

    try:
        return call_llm(prompt)
    except Exception as e:
        return f"Gap analysis error: {str(e)}"