from app.services.llm_service import call_llm


def generate_full_report(topic, papers):

    print("⚡ FAST MODE (single LLM call)")

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:300]}"
        for p in papers
    ])[:2000]

    prompt = f"""
You are a team of research experts.

Topic: {topic}

Provide:

1. Key Insights
2. Common Themes
3. Summary
4. Research Gaps

Be concise and structured.

Papers:
{content}
"""

    return call_llm(prompt)