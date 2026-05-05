from app.services.llm_service import call_llm


def synthesize(topic, papers):
    print("🧠 Cross-paper synthesis working...")

    if not papers:
        return "No data available for synthesis."

    # -----------------------------
    # STEP 1: COLLECT ALL POINTS
    # -----------------------------
    all_points = []
    all_keywords = []

    for p in papers:
        insights = p.get("insights", {})

        points = insights.get("points", [])
        keywords = insights.get("keywords", [])

        all_points.extend(points)
        all_keywords.extend(keywords)

    # -----------------------------
    # STEP 2: SIMPLE DEDUPLICATION
    # -----------------------------
    unique_points = list(set([p.strip().lower() for p in all_points if p]))
    unique_keywords = list(set([k.strip().lower() for k in all_keywords if k]))

    # limit size (important for LLM)
    unique_points = unique_points[:20]
    unique_keywords = unique_keywords[:20]

    # -----------------------------
    # STEP 3: BUILD STRUCTURED INPUT
    # -----------------------------
    content = f"""
Key Ideas Across Papers:
- {"; ".join(unique_points[:15])}

Common Keywords:
- {", ".join(unique_keywords[:15])}
"""

    # -----------------------------
    # STEP 4: PROMPT (SMART)
    # -----------------------------
    prompt = f"""
You are an expert research synthesizer.

Topic: {topic}

Given aggregated insights from multiple papers:

{content}

Generate:

1. Core Consensus (what most papers agree on)
2. Key Differences (where papers diverge)
3. Important Concepts (central ideas)
4. Emerging Trends
5. Final Synthesis (2-3 sentences)

Rules:
- Do NOT repeat same points
- Combine ideas intelligently
- Be concise
- Focus on cross-paper understanding
"""

    # -----------------------------
    # STEP 5: LLM CALL
    # -----------------------------
    try:
        result = call_llm(prompt)

        if not result or len(result.strip()) < 20:
            return "Synthesis not available"

        return result

    except Exception as e:
        print("⚠️ Synthesis error:", str(e))
        return "Synthesis temporarily unavailable"