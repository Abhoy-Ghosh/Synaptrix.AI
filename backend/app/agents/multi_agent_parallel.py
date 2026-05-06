import asyncio

from app.agents.summarizer import summarize
from app.agents.analyzer import analyze
from app.agents.gap_finder import find_gaps


async def run_multi_agent_parallel(topic, papers):

    print("⚡ Parallel Research Pipeline Started")

    # -----------------------------
    # GUARD CLAUSE
    # -----------------------------
    if not papers:
        return {
            "summary": "No papers available",
            "analysis": "No analysis available",
            "gaps": "No research gaps available"
        }

    loop = asyncio.get_running_loop()

    # -----------------------------
    # PARALLEL TASK EXECUTION
    # -----------------------------
    summary_task = loop.run_in_executor(
        None,
        summarize,
        topic,
        papers
    )

    analysis_task = loop.run_in_executor(
        None,
        analyze,
        topic,
        papers
    )

    gaps_task = loop.run_in_executor(
        None,
        find_gaps,
        topic,
        papers
    )

    # -----------------------------
    # SAFE PARALLEL GATHER
    # -----------------------------
    results = await asyncio.gather(
        summary_task,
        analysis_task,
        gaps_task,
        return_exceptions=True
    )

    summary, analysis, gaps = results

    # -----------------------------
    # FAILURE HANDLING
    # -----------------------------
    if isinstance(summary, Exception):
        print("⚠️ Summary Agent Failed:", str(summary))

        summary = """
# Research Summary

- Summary generation temporarily unavailable
"""

    if isinstance(analysis, Exception):
        print("⚠️ Analyzer Agent Failed:", str(analysis))

        analysis = """
# Research Analysis

## Key Patterns
- Analysis generation temporarily unavailable
"""

    if isinstance(gaps, Exception):
        print("⚠️ Gap Finder Agent Failed:", str(gaps))

        gaps = """
# Research Gap Analysis

## Research Gaps
- Gap analysis temporarily unavailable
"""

    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------
    return {
        "topic": topic,
        "status": "success",
        "agents_used": [
            "summarizer",
            "analyzer",
            "gap_finder"
        ],
        "summary": summary,
        "analysis": analysis,
        "gaps": gaps
    }