from app.services.llm_service import call_llm


def analyze(topic, papers):
    print("🤖 Analyzer Agent working...")

    if not papers:
        return "No papers available for analysis."

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:200]}"
        for p in papers
    ])[:2500]

    prompt = f"""
You are an elite AI Research Intelligence Analyst.

Your task is to analyze ONLY the provided research papers for the topic below.

========================
RESEARCH TOPIC
========================
{topic}

========================
STRICT INSTRUCTIONS
========================
- ONLY use information from the provided papers
- Do NOT introduce unrelated domains
- Do NOT hallucinate facts
- If evidence is weak, explicitly mention uncertainty
- Stay fully grounded in the paper abstracts
- Keep insights concise, technical, and research-focused
- Avoid generic AI buzzwords
- Prefer specific observations over vague summaries
- Use clean hierarchical markdown formatting
- Output MUST be frontend-render friendly
- Each section MUST contain bullet points
- Keep each bullet under 2 lines
- Maximum 5 bullets per section

========================
OUTPUT FORMAT
========================

# Research Analysis

## Key Patterns
- Pattern 1
- Pattern 2

## Emerging Trends
- Trend 1
- Trend 2

## Research Agreements
- Agreement 1
- Agreement 2

## Research Disagreements
- Disagreement 1
- Disagreement 2

## Methodological Observations
- Observation 1
- Observation 2

## Strategic Insights
- Insight 1
- Insight 2

## Research Limitations
- Limitation 1
- Limitation 2

========================
QUALITY RULES
========================

GOOD OUTPUT:
- "Most papers emphasize human oversight in autonomous warfare systems"

BAD OUTPUT:
- "AI is transforming industries globally"

GOOD OUTPUT:
- "Several papers discuss ethical constraints for AI-driven military decision-making"

BAD OUTPUT:
- "Healthcare datasets require preprocessing"

========================
PAPERS
========================
{content}
"""

    try:
        result = call_llm(prompt)

        if not result or len(result.strip()) < 20:
            return "Analysis not available"

        # Structure validation
        if "Key Patterns" not in result:
            print("⚠️ Analyzer format issue → using fallback")

            return """
# Research Analysis

## Key Patterns
- Patterns could not be clearly extracted

## Emerging Trends
- Trends not clearly identified

## Research Agreements
- Research alignment unclear

## Research Disagreements
- Mixed or conflicting findings

## Methodological Observations
- Methodological insights unavailable

## Strategic Insights
- Strategic interpretation unavailable

## Research Limitations
- Limitations not clearly discussed
"""

        return result.strip()

    except Exception as e:
        print("⚠️ Analyzer error:", str(e))
        return "Analysis temporarily unavailable"