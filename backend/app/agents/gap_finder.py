from app.services.llm_service import call_llm


def find_gaps(topic, papers):
    print("🤖 Gap Finder Agent working...")

    if not papers:
        return "No papers available to identify research gaps."

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:200]}"
        for p in papers
    ])[:2000]  # 🔥 limit prompt size

    prompt = f"""
You are a research strategist.

Topic: {topic}

Analyze the papers and identify:

Research Gaps:
- Missing or under-explored areas

Future Directions:
- Promising areas for future research

Limitations:
- Common weaknesses or constraints in current work

Rules:
- Use bullet points
- Keep it concise
- Max 5 points per section

Papers:
{content}
"""

    try:
        result = call_llm(prompt)

        # 🔥 basic validation
        if not result or len(result.strip()) < 20:
            return "Gap analysis not available"

        return result

    except Exception as e:
        print("⚠️ Gap Finder error:", str(e))
        return "Gap analysis temporarily unavailable"