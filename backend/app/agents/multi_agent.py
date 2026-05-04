from app.agents.summarizer import summarize
from app.agents.analyzer import analyze
from app.agents.gap_finder import find_gaps


async def run_multi_agent(topic, papers):

    print("🧠 Sequential research mode")

    summary = summarize(topic, papers)
    analysis = analyze(topic, papers)
    gaps = find_gaps(topic, papers)

    return {
        "summary": summary,
        "analysis": analysis,
        "gaps": gaps
    }