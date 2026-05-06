from app.services.llm_service import call_llm
from app.agents.clusterer import cluster_papers


def synthesize(topic, papers):

    print("🧠 Cluster-based synthesis working...")

    if not papers:
        return "No data available"

    # =========================================================
    # STEP 1 — CLUSTER PAPERS
    # =========================================================
    clusters = cluster_papers(papers)

    cluster_summaries = []

    # =========================================================
    # STEP 2 — BUILD CLUSTER SUMMARIES
    # =========================================================
    for idx, cluster in enumerate(clusters):

        points = []

        for p in cluster:

            insights = p.get("insights", {})

            points.extend(
                insights.get("points", [])
            )

        unique_points = list(set(points))[:10]

        cluster_summaries.append({
            "cluster_id": idx,
            "size": len(cluster),
            "points": unique_points
        })

    # =========================================================
    # STEP 3 — BUILD SYNTHESIS CONTEXT
    # =========================================================
    content = ""

    for c in cluster_summaries:

        content += f"""

Cluster {c['cluster_id']} (size: {c['size']}):

"""

        # IMPORTANT:
        # preserve semantic structure
        for point in c["points"]:

            content += f"- {point}\n"

        content += "\n"

    # Larger context for synthesis reasoning
    content = content[:5000]

    # =========================================================
    # STEP 4 — SYNTHESIS PROMPT
    # =========================================================
    prompt = f"""
You are an elite AI Research Synthesis Engine.

Your task is to synthesize research intelligence
ONLY from the provided cluster summaries.

RESEARCH TOPIC:
{topic}

INSTRUCTIONS:
- ONLY use the supplied cluster information
- Stay grounded in the cluster insights
- Compare clusters instead of repeating points
- Identify similarities and differences
- Highlight recurring research directions
- Detect conflicting approaches if present
- Avoid generic AI statements
- Keep outputs concise and technical
- Use clean markdown formatting
- Every section MUST contain bullet points
- Maximum 5 bullets per section

OUTPUT FORMAT:

# Cluster Intelligence

## Cluster Relationships
- ...

## Contrasting Research Directions
- ...

## Emerging Trends
- ...

## Cross-Domain Insights
- ...

## Strategic Observations
- ...

## Unified Research Understanding
- 2-3 concise synthesis sentences

CLUSTER DATA:
{content}
"""

    try:

        result = call_llm(prompt)

        if not result or len(result.strip()) < 20:
            return "Synthesis not available"

        # =====================================================
        # DEBUG RAW OUTPUT
        # =====================================================
        print("\n============= SYNTHESIS RAW =============\n")
        print(result)
        print("\n=========================================\n")

        # =====================================================
        # RELAXED VALIDATION
        # =====================================================
        required_sections = [
            "cluster relationships",
            "emerging trends",
            "strategic observations"
        ]

        normalized = result.lower()

        if not all(
            section in normalized
            for section in required_sections
        ):

            print("⚠️ Synthesis structure incomplete")

            return result.strip()

        return result.strip()

    except Exception as e:

        print("⚠️ Synthesis error:", str(e))

        return "Synthesis failed"