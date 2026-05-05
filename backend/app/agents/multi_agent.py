from app.agents.summarizer import summarize
from app.agents.analyzer import analyze
from app.agents.gap_finder import find_gaps


def _safe(text, fallback):
    if not text or len(str(text).strip()) < 20:
        return fallback
    return text


async def run_multi_agent(topic, papers):

    print("🧠 Sequential research mode (reasoning chain)")

    # -----------------------------
    # STEP 1: SUMMARY
    # -----------------------------
    summary = summarize(topic, papers)
    summary = _safe(summary, "Summary not available")

    # -----------------------------
    # STEP 2: ANALYSIS
    # -----------------------------
    analysis_input = f"""
Topic: {topic}

Use the following summary to improve reasoning:

{summary}
"""

    analysis = analyze(analysis_input, papers)
    analysis = _safe(analysis, "Analysis not available")

    # -----------------------------
    # STEP 3: GAPS
    # -----------------------------
    gaps_input = f"""
Topic: {topic}

Use both summary and analysis:

Summary:
{summary}

Analysis:
{analysis}
"""

    gaps = find_gaps(gaps_input, papers)
    gaps = _safe(gaps, "Gap analysis not available")

    return {
        "summary": summary,
        "analysis": analysis,
        "gaps": gaps
    }