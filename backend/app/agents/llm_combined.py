from app.services.llm_service import call_llm


def generate_full_report(topic, papers):

    print("⚡ FAST MODE (single LLM call)")

    if not papers:
        return "No papers available."

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:300]}"
        for p in papers
    ])[:2000]

    prompt = f"""
You are a team of research experts.

Topic: {topic}

Return output STRICTLY in this format:

Key Insights:
- ...
- ...

Common Themes:
- ...
- ...

Summary:
- 2-3 sentences

Research Gaps:
- ...
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
            return "Report not available"

        # 🔥 STRUCTURE CHECK
        if "Key Insights" not in result:
            print("⚠️ Fast mode format issue → using fallback")

            return f"""
Key Insights:
- Could not extract insights reliably

Common Themes:
- Themes not clearly identified

Summary:
- Summary unavailable due to formatting issue

Research Gaps:
- Gaps could not be determined
"""

        return result.strip()

    except Exception as e:
        print("⚠️ Fast mode error:", str(e))
        return "Report temporarily unavailable"