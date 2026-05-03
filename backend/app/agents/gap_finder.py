from app.services.llm_service import summarize_papers


def find_gaps(topic, papers):
    print("🤖 Gap Finder Agent working...")

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:200]}"
        for p in papers
    ])

    prompt = f"""
You are a research strategist.

Topic: {topic}

Identify:
- Missing areas in research
- Under-explored topics
- Opportunities for innovation

Papers:
{content}
"""

    try:
        return summarize_papers(papers, topic)
    except Exception as e:
        return f"Gap analysis error: {str(e)}"