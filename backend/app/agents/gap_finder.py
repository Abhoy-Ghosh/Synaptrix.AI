from app.services.llm_service import call_llm


def find_gaps(topic, papers):
    print("🤖 Gap Finder Agent working...")

    if not papers:
        return "No papers available to identify research gaps."

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:200]}"
        for p in papers
    ])[:2000]

    prompt = f"""
You are a research strategist.

Topic: {topic}

Return output STRICTLY in this format:

Research Gaps:
- ...
- ...

Future Directions:
- ...
- ...

Limitations:
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
            return "Gap analysis not available"

        # 🔥 STRUCTURE VALIDATION
        if "Research Gaps" not in result:
            print("⚠️ Gap format issue → using fallback")

            return f"""
Research Gaps:
- Could not clearly identify gaps

Future Directions:
- Further research needed

Limitations:
- Current literature insufficient for detailed analysis
"""

        return result.strip()

    except Exception as e:
        print("⚠️ Gap Finder error:", str(e))
        return "Gap analysis temporarily unavailable"