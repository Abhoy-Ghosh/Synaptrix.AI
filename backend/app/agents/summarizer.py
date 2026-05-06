from app.services.llm_service import call_llm


def summarize_papers(papers, topic):

    if not papers:
        return "No papers available for summarization."

    content = "\n\n".join([
        f"{p['title']}: {p['abstract'][:300]}"
        for p in papers
    ])[:2500]

    prompt = f"""
You are an elite AI Research Summarization Expert.

Your task is to summarize ONLY the provided research papers
for the given research topic.

========================
RESEARCH TOPIC
========================
{topic}

========================
STRICT INSTRUCTIONS
========================
- ONLY use information from the provided papers
- Do NOT introduce unrelated domains
- Do NOT hallucinate findings
- Stay grounded in the paper abstracts
- Avoid generic AI statements
- Prefer specific technical observations
- Focus on major findings, methodologies, and recurring themes
- Keep outputs concise and structured
- Use frontend-friendly markdown formatting
- Every section MUST contain bullet points
- Maximum 5 bullets per section
- Each bullet should remain under 2 lines
- No introductory or concluding paragraphs
- If evidence is weak, explicitly mention uncertainty

========================
OUTPUT FORMAT
========================

# Research Summary

## Key Insights
- Insight 1
- Insight 2

## Common Themes
- Theme 1
- Theme 2

## Emerging Focus Areas
- Area 1
- Area 2

## Summary
- 2-3 concise research-focused sentences

========================
QUALITY RULES
========================

GOOD OUTPUT:
- "Most papers emphasize maintaining human oversight in autonomous AI systems"

BAD OUTPUT:
- "AI is transforming the world"

GOOD OUTPUT:
- "Several studies focus on ethical governance of AI-assisted military decision-making"

BAD OUTPUT:
- "Technology is evolving rapidly"

GOOD OUTPUT:
- "Research attention is shifting toward explainability and operational safety"

BAD OUTPUT:
- "Many future opportunities exist"

========================
PAPERS
========================
{content}
"""

    try:
        result = call_llm(prompt)

        if not result or len(result.strip()) < 20:
            return "Summary not available"

        # Structure validation
        if "Key Insights" not in result:
            print("⚠️ Summarizer format issue → using fallback")

            return """
# Research Summary

## Key Insights
- Insights could not be extracted

## Common Themes
- Themes not clearly identified

## Emerging Focus Areas
- Research focus areas unavailable

## Summary
- Summary unavailable due to formatting issue
"""

        return result.strip()

    except Exception as e:
        print("⚠️ Summarizer error:", str(e))
        return "Summary temporarily unavailable"


# -----------------------------
# AGENT ENTRY
# -----------------------------
def summarize(topic, papers):
    print("🤖 Summarizer Agent working...")
    return summarize_papers(papers, topic)