from app.services.llm_service import call_llm
from app.agents.clusterer import cluster_papers


def synthesize(topic, papers):
    print("🧠 Cluster-based synthesis working...")

    if not papers:
        return "No data available"

    # -----------------------------
    # STEP 1: CLUSTER
    # -----------------------------
    clusters = cluster_papers(papers)

    cluster_summaries = []

    # -----------------------------
    # STEP 2: SUMMARIZE EACH CLUSTER
    # -----------------------------
    for idx, cluster in enumerate(clusters):
        points = []

        for p in cluster:
            insights = p.get("insights", {})
            points.extend(insights.get("points", []))

        unique_points = list(set(points))[:10]

        cluster_summaries.append({
            "cluster_id": idx,
            "size": len(cluster),
            "points": unique_points
        })

    # -----------------------------
    # STEP 3: BUILD INPUT
    # -----------------------------
    content = ""

    for c in cluster_summaries:
        content += f"""
Cluster {c['cluster_id']} (size: {c['size']}):
- {'; '.join(c['points'])}
"""

    content = content[:3000]

    # -----------------------------
    # STEP 4: FINAL SYNTHESIS
    # -----------------------------
    prompt = f"""
You are an expert research synthesizer.

Topic: {topic}

Clusters represent groups of similar papers.

{content}

Generate:

1. Cluster-wise Insights
2. Differences Between Clusters
3. Overall Trends
4. Final Unified Understanding

Rules:
- Compare clusters (not individual points)
- Highlight contradictions between clusters
- Avoid repetition
"""

    try:
        result = call_llm(prompt)

        if not result or len(result.strip()) < 20:
            return "Synthesis not available"

        return result

    except Exception as e:
        print("⚠️ Synthesis error:", str(e))
        return "Synthesis failed"