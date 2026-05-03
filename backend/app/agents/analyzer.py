from app.services.llm_service import summarize_papers

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
- Conflicting ideas
- Gaps in research
- Future opportunities

Papers:
{content}
"""

    try:
        return summarize_papers(papers, topic)  # reuse LLM
    except Exception as e:
        return f"Analysis error: {str(e)}"