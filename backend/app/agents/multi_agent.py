from app.agents.summarizer import summarize
from app.agents.analyzer import analyze
from app.agents.gap_finder import find_gaps


def _safe(text, fallback):
    if not text or len(str(text).strip()) < 20:
        return fallback
    return text


def _compress_context(text, limit=500):
    """
    Prevents context explosion and hallucination drift
    while still preserving reasoning-chain behavior.
    """
    if not text:
        return ""

    return text.strip()[:limit]


async def run_multi_agent(topic, papers):

    print("🧠 Advanced Sequential Research Mode")

    # -----------------------------
    # GUARD CLAUSE
    # -----------------------------
    if not papers:
        return {
            "summary": "No papers available",
            "analysis": "No analysis available",
            "gaps": "No gap analysis available"
        }

    # =========================================================
    # STEP 1 — SUMMARY AGENT
    # =========================================================
    summary = summarize(topic, papers)

    summary = _safe(
        summary,
        """
# Research Summary

- Summary not available
"""
    )

    # ---------------------------------------------------------
    # LIGHTWEIGHT MEMORY COMPRESSION
    # ---------------------------------------------------------
    compressed_summary = _compress_context(summary)

    # =========================================================
    # STEP 2 — ANALYZER AGENT
    # =========================================================
    analysis_topic = f"""
Research Topic:
{topic}

Reference Summary (context only):
{compressed_summary}

Instructions:
- Use the summary only as lightweight reasoning context
- Primary grounding MUST come from the research papers
- Do NOT repeat the summary directly
- Do NOT introduce unrelated domains
"""

    analysis = analyze(analysis_topic, papers)

    analysis = _safe(
        analysis,
        """
# Research Analysis

## Key Patterns
- Analysis not available
"""
    )

    # ---------------------------------------------------------
    # COMPRESS ANALYSIS
    # ---------------------------------------------------------
    compressed_analysis = _compress_context(analysis)

    # =========================================================
    # STEP 3 — GAP FINDER AGENT
    # =========================================================
    gaps_topic = f"""
Research Topic:
{topic}

Reference Summary:
{compressed_summary}

Reference Analysis:
{compressed_analysis}

Instructions:
- Use previous outputs only as lightweight reasoning aids
- Primary grounding MUST come from the research papers
- Focus on missing research, limitations, and future opportunities
- Avoid generic AI statements
- Do NOT introduce unrelated domains
"""

    gaps = find_gaps(gaps_topic, papers)

    gaps = _safe(
        gaps,
        """
# Research Gap Analysis

## Research Gaps
- Gap analysis not available
"""
    )

    # =========================================================
    # FINAL RESPONSE
    # =========================================================
    return {
        "topic": topic,
        "mode_used": "advanced_reasoning",
        "pipeline_version": "v3",
        "agents_used": [
            "summarizer",
            "analyzer",
            "gap_finder"
        ],
        "reasoning_chain": [
            "summary -> analysis -> gaps"
        ],
        "summary": summary,
        "analysis": analysis,
        "gaps": gaps
    }