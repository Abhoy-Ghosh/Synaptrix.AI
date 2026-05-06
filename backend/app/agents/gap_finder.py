from app.services.llm_service import call_llm


def find_gaps(topic, papers):
    print("🤖 Gap Finder Agent working...")

    if not papers:
        return "No papers available to identify research gaps."

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:200]}"
        for p in papers
    ])[:2500]

    prompt = f"""
You are an elite AI Research Gap Analyst and Research Strategy Expert.

Your task is to identify research gaps, limitations, and future opportunities
ONLY from the provided research papers.

========================
RESEARCH TOPIC
========================
{topic}

========================
STRICT INSTRUCTIONS
========================
- ONLY use information from the provided papers
- Do NOT introduce unrelated domains
- Do NOT hallucinate missing research areas
- Stay grounded in the supplied abstracts
- If evidence is weak, explicitly mention uncertainty
- Focus on missing methodologies, unanswered questions, weak evaluations, scalability issues, ethical concerns, or deployment limitations
- Avoid generic AI statements
- Prefer concrete technical observations
- Keep outputs concise and structured
- Use frontend-friendly hierarchical markdown
- Every section MUST contain bullet points
- Maximum 5 bullets per section
- Each bullet should remain under 2 lines
- No paragraph explanations
- No introductory or concluding text

========================
OUTPUT FORMAT
========================

# Research Gap Analysis

## Research Gaps
- Gap 1
- Gap 2

## Future Research Directions
- Direction 1
- Direction 2

## Methodological Weaknesses
- Weakness 1
- Weakness 2

## Deployment Challenges
- Challenge 1
- Challenge 2

## Strategic Opportunities
- Opportunity 1
- Opportunity 2

========================
QUALITY RULES
========================

GOOD OUTPUT:
- "Most papers lack real-world deployment validation for autonomous military systems"

BAD OUTPUT:
- "AI still has many challenges"

GOOD OUTPUT:
- "Limited discussion exists around adversarial robustness in AI warfare systems"

BAD OUTPUT:
- "Technology is evolving rapidly"

GOOD OUTPUT:
- "Few studies evaluate long-term ethical implications of autonomous decision-making"

BAD OUTPUT:
- "More research is needed"

========================
PAPERS
========================
{content}
"""

    try:
        result = call_llm(prompt)

        if not result or len(result.strip()) < 20:
            return "Gap analysis not available"

        # Structure validation
        if "Research Gaps" not in result:
            print("⚠️ Gap format issue → using fallback")

            return """
# Research Gap Analysis

## Research Gaps
- Could not clearly identify research gaps

## Future Research Directions
- Additional investigation required

## Methodological Weaknesses
- Methodological insights unavailable

## Deployment Challenges
- Deployment-related findings unclear

## Strategic Opportunities
- Strategic opportunities not clearly identified
"""

        return result.strip()

    except Exception as e:
        print("⚠️ Gap Finder error:", str(e))
        return "Gap analysis temporarily unavailable"