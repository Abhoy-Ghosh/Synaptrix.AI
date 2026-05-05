import asyncio
from app.agents.summarizer import summarize
from app.agents.analyzer import analyze
from app.agents.gap_finder import find_gaps


async def run_multi_agent_parallel(topic, papers):

    print("⚡ Parallel mode")

    loop = asyncio.get_running_loop()

    # -----------------------------
    # RUN TASKS
    # -----------------------------
    summary_task = loop.run_in_executor(None, summarize, topic, papers)
    analysis_task = loop.run_in_executor(None, analyze, topic, papers)
    gaps_task = loop.run_in_executor(None, find_gaps, topic, papers)

    # -----------------------------
    # SAFE GATHER
    # -----------------------------
    results = await asyncio.gather(
        summary_task,
        analysis_task,
        gaps_task,
        return_exceptions=True  # 🔥 IMPORTANT
    )

    summary, analysis, gaps = results

    # -----------------------------
    # HANDLE FAILURES
    # -----------------------------
    if isinstance(summary, Exception):
        print("⚠️ Summary failed:", summary)
        summary = "Summary not available"

    if isinstance(analysis, Exception):
        print("⚠️ Analysis failed:", analysis)
        analysis = "Analysis not available"

    if isinstance(gaps, Exception):
        print("⚠️ Gaps failed:", gaps)
        gaps = "Gap analysis not available"

    return {
        "summary": summary,
        "analysis": analysis,
        "gaps": gaps
    }