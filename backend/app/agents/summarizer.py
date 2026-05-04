from app.services.llm_service import call_llm


def summarize_papers(papers, topic):
    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:300]}"
        for p in papers
    ])[:2000]

    prompt = f"""
You are a research summarization expert.

Topic: {topic}

Give:
1. Key insights
2. Common themes
3. Short summary

Papers:
{content}
"""

    result = call_llm(prompt)

    if "quota" in str(result).lower():
        return "⚠️ Summary unavailable (LLM quota exceeded)"

    return result


# 🔥 ADD THIS (IMPORTANT)
def summarize(topic, papers):
    print("🤖 Summarizer Agent working...")
    return summarize_papers(papers, topic)