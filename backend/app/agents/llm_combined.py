from app.services.llm_service import call_llm


def generate_full_report(topic, papers):

    print("⚡ FAST MODE (single LLM call)")

    if not papers:
        return "No papers available."

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:300]}"
        for p in papers
    ])[:2500]

    prompt = f"""
You are an elite AI Research Synthesis Engine.

Your task is to generate a complete research intelligence report
ONLY from the provided research papers.

========================
RESEARCH TOPIC
========================
{topic}

========================
STRICT INSTRUCTIONS
========================
- ONLY use information from the supplied papers
- Do NOT introduce unrelated domains
- Do NOT hallucinate facts or methodologies
- Stay grounded in the paper abstracts
- Avoid generic AI statements
- Prefer specific technical observations
- Focus on findings, methodologies, trends, limitations, and strategic implications
- Keep outputs concise and structured
- Use frontend-friendly markdown formatting
- Every section MUST contain bullet points
- Each bullet should remain under 2 lines
- Maximum 5 bullets per section
- No introductory or concluding paragraphs
- If evidence is weak, explicitly mention uncertainty

========================
OUTPUT FORMAT
========================

# Research Intelligence Report

## Key Insights
- Insight 1
- Insight 2

## Common Themes
- Theme 1
- Theme 2

## Emerging Trends
- Trend 1
- Trend 2

## Research Summary
- 2-3 concise research-focused sentences

## Research Gaps
- Gap 1
- Gap 2

## Strategic Importance
- Strategic insight 1
- Strategic insight 2

========================
QUALITY RULES
========================

GOOD OUTPUT:
- "Several papers emphasize maintaining human oversight in autonomous warfare systems"

BAD OUTPUT:
- "AI is transforming many industries"

GOOD OUTPUT:
- "Research focuses heavily on ethical governance of AI-enabled military decision-making"

BAD OUTPUT:
- "Technology is rapidly evolving"

GOOD OUTPUT:
- "Limited real-world validation exists for autonomous combat decision systems"

BAD OUTPUT:
- "More studies are needed"

========================
PAPERS
========================
{content}
"""

    try:
        result = call_llm(prompt)

        if not result or len(result.strip()) < 20:
            return "Report not available"

        # Structure validation
        if "Key Insights" not in result:
            print("⚠️ Fast mode format issue → using fallback")

            return """
# Research Intelligence Report

## Key Insights
- Could not reliably extract insights

## Common Themes
- Themes not clearly identified

## Emerging Trends
- Trends unavailable

## Research Summary
- Summary unavailable due to formatting issue

## Research Gaps
- Research gaps could not be determined

## Strategic Importance
- Strategic interpretation unavailable
"""

        return result.strip()

    except Exception as e:
        print("⚠️ Fast mode error:", str(e))
        return "Report temporarily unavailable"