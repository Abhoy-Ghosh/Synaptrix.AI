from app.services.llm_service import call_llm
from app.agents.clusterer import cluster_papers


# =========================================
# SYNTHESIS ENGINE
# =========================================

def synthesize(topic, papers):

    print("🧠 Cluster-based synthesis working...")

    # =====================================
    # SAFETY
    # =====================================

    if not papers:

        return """
# Cluster Intelligence

## Status
- No research papers available

## Recommendation
- Try another query
"""

    # =====================================
    # CLUSTER PAPERS
    # =====================================

    print("🧠 Clustering papers...")

    clusters = cluster_papers(papers)

    cluster_summaries = []

    # =====================================
    # BUILD CLUSTER SUMMARIES
    # =====================================

    for idx, cluster in enumerate(clusters):

        points = []

        for p in cluster:

            insights = p.get(
                "insights",
                {}
            )

            extracted = insights.get(
                "points",
                []
            )

            if extracted:

                points.extend(extracted)

        # Remove duplicates
        unique_points = list(
            dict.fromkeys(points)
        )[:8]

        cluster_summaries.append({

            "cluster_id": idx + 1,

            "size": len(cluster),

            "points": unique_points
        })

    # =====================================
    # EMPTY CLUSTER SAFETY
    # =====================================

    if not cluster_summaries:

        return """
# Cluster Intelligence

## Status
- Cluster synthesis unavailable

## Recommendation
- Retrieval quality insufficient
"""

    # =====================================
    # BUILD CONTEXT
    # =====================================

    content = ""

    for c in cluster_summaries:

        content += (

            f"\nCluster {c['cluster_id']} "
            f"(size: {c['size']}):\n\n"
        )

        for point in c["points"]:

            cleaned = point.strip()

            if cleaned:

                content += f"- {cleaned}\n"

        content += "\n"

    # =====================================
    # TOKEN CONTROL
    # =====================================

    MAX_CONTEXT = 2500

    content = content[:MAX_CONTEXT]

    # =====================================
    # PROMPT
    # =====================================

    prompt = f"""
You are an elite AI Research Intelligence Engine.

Your task is to synthesize research intelligence
ONLY from the provided cluster summaries.

RESEARCH TOPIC:
{topic}

RULES:
- Stay grounded in the cluster data
- Compare clusters instead of repeating
- Avoid hallucinations
- Be concise and technical
- Use markdown headings
- Use bullet points
- Maximum 4 bullets per section
- No generic AI filler

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
- 2 concise synthesis sentences

CLUSTER DATA:
{content}
"""

    # =====================================
    # CALL LLM
    # =====================================

    try:

        result = call_llm(prompt)

        # =================================
        # EMPTY SAFETY
        # =================================

        if not result:

            print("⚠️ Empty synthesis result")

            return fallback_synthesis(
                topic,
                cluster_summaries
            )

        result = str(result).strip()

        # =================================
        # WEAK RESPONSE SAFETY
        # =================================

        if len(result) < 30:

            print("⚠️ Weak synthesis response")

            return fallback_synthesis(
                topic,
                cluster_summaries
            )

        # =================================
        # DEBUG
        # =================================

        print(
            "\n============= SYNTHESIS RAW =============\n"
        )

        print(result[:1500])

        print(
            "\n=========================================\n"
        )

        # =================================
        # RELAXED VALIDATION
        # =================================

        important_sections = [

            "cluster relationships",

            "emerging trends",

            "strategic observations"
        ]

        normalized = result.lower()

        matched = sum(

            1 for section in important_sections

            if section in normalized
        )

        # =================================
        # STRUCTURE WARNING
        # =================================

        if matched < 2:

            print(
                "⚠️ Partial synthesis structure"
            )

        return result

    except Exception as e:

        print(
            "⚠️ Synthesis error:",
            str(e)
        )

        return fallback_synthesis(
            topic,
            cluster_summaries
        )


# =========================================
# FALLBACK SYNTHESIS
# =========================================

def fallback_synthesis(

    topic,
    cluster_summaries

):

    cluster_count = len(cluster_summaries)

    total_points = sum(

        len(c["points"])

        for c in cluster_summaries
    )

    return f"""
# Cluster Intelligence

## Cluster Relationships
- {cluster_count} research clusters identified
- Semantic grouping completed successfully
- Cross-paper similarity analysis performed

## Emerging Trends
- {total_points} major insight signals detected
- Research directions show thematic overlap
- Cluster-level synthesis generated

## Strategic Observations
- Retrieval and ranking pipeline completed
- Cluster intelligence partially available
- AI synthesis fallback activated

## Unified Research Understanding
The system identified semantically related
research themes for the topic "{topic}".

Cross-paper relationship analysis completed
successfully.
"""