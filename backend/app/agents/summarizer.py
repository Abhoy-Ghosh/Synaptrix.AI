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

Return output STRICTLY in this format:

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
- Max 5 points per section
- No extra text outside sections

Papers:
{content}
"""

    try:
        result = call_llm(prompt)

        if not result or len(result.strip()) < 20:
            return "Summary not available"

        # 🔥 STRUCTURE VALIDATION
        if "Key Insights" not in result:
            print("⚠️ Summarizer format issue → using fallback")

            return f"""
Key Insights:
- Insights could not be extracted

Common Themes:
- Themes not clearly identified

Summary:
- Summary unavailable due to formatting issue
"""

        return result.strip()

    except Exception as e:
        print("⚠️ Summarizer error:", str(e))
        return "Summary temporarily unavailable"


# -----------------------------
# AGENT ENTRY
# -----------------------------
def summarize(topic, papers):
    print("🤖 Summarizer Agent working...")
    return summarize_papers(papers, topic)