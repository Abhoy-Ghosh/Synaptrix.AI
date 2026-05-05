from app.services.llm_service import call_llm


def summarize_papers(papers, topic):
    if not papers:
        return "No papers available for summarization."

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:300]}"
        for p in papers
    ])[:2000]

    prompt = f"""
You are a research summarization expert.

Topic: {topic}

Provide output in this format:

Key Insights:
- ...
- ...

Common Themes:
- ...
- ...

Summary:
- 2–3 concise sentences

Rules:
- Use bullet points
- Keep it clear and short

Papers:
{content}
"""

    try:
        result = call_llm(prompt)

        # 🔥 Basic validation
        if not result or len(result.strip()) < 20:
            return "Summary not available"

        return result

    except Exception as e:
        print("⚠️ Summarizer error:", str(e))
        return "Summary temporarily unavailable"


# -----------------------------
# AGENT ENTRY
# -----------------------------
def summarize(topic, papers):
    print("🤖 Summarizer Agent working...")
    return summarize_papers(papers, topic)