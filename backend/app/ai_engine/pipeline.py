from app.agents.retriever import retrieve_papers
from app.agents.summarizer import summarize
from app.agents.analyzer import analyze
from app.agents.similarity import find_similarities
from app.agents.gap_finder import find_gaps
from app.agents.insight_extractor import extract_insights

from app.cache.cache import get_cached_result, set_cached_result, delete_cached_result
from app.retrieval.vector_store import add_to_index, search_index
from app.feedback.feedback_store import get_feedback
from app.feedback.paper_feedback import get_paper_score

from sentence_transformers import SentenceTransformer
import numpy as np
import asyncio
import time

# -----------------------------
# NORMALIZE
# -----------------------------
def normalize_topic(topic):
    return topic.strip().lower()


# -----------------------------
# MODEL
# -----------------------------
model = None

def get_model():
    global model
    if model is None:
        print("🔥 Loading embedding model...")
        start = time.time()
        model = SentenceTransformer('all-mpnet-base-v2', device='cpu')
        print("Model load time:", time.time() - start)
    return model


# -----------------------------
# WARMUP
# -----------------------------
def warmup_model():
    get_model()
    print("✅ Embedding model warm")


# -----------------------------
# DEDUP
# -----------------------------
def deduplicate(papers):
    seen = set()
    unique = []
    for p in papers:
        if p["title"] not in seen:
            seen.add(p["title"])
            unique.append(p)
    return unique


# -----------------------------
# QUALITY CHECK
# -----------------------------
def is_good_result(results):
    return len(results) >= 3


# -----------------------------
# KEYWORD SCORE
# -----------------------------
def keyword_score(text, topic):
    text = text.lower()
    topic_words = topic.lower().split()
    score = sum(1 for w in topic_words if w in text)
    return score / max(len(topic_words), 1)


# -----------------------------
# FILTER
# -----------------------------
def filter_relevant(papers, topic):
    topic_words = topic.lower().split()
    filtered = []
    for p in papers:
        text = p["abstract"].lower()
        if any(word in text for word in topic_words):
            filtered.append(p)
    return filtered


# -----------------------------
# HYBRID RANKING
# -----------------------------
def rerank_hybrid(papers, topic, query_embedding, embeddings):
    final_scores = []

    for i, paper in enumerate(papers):
        emb = embeddings[i]

        semantic = np.dot(emb, query_embedding) / (
            np.linalg.norm(emb) * np.linalg.norm(query_embedding)
        )

        keyword = keyword_score(paper["abstract"], topic)
        feedback = min(get_paper_score(paper["title"]), 1.0) * 0.15
        title_boost = 0.1 if topic.lower() in paper["title"].lower() else 0
        phrase_boost = 0.1 if topic.lower() in paper["abstract"].lower() else 0
        citation_boost = min(paper.get("citations", 0) / 1000, 1.0) * 0.1
        recency_boost = (2025 - paper.get("year", 2020)) * -0.02
        source_boost = 0.05 if paper.get("source") == "semantic" else 0

        final = (
            0.5 * semantic +
            0.2 * keyword +
            0.15 * feedback +
            0.1 * citation_boost +
            source_boost +
            recency_boost +
            title_boost +
            phrase_boost
        )

        final_scores.append((final, paper))

    final_scores.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in final_scores]


# -----------------------------
# MODE SELECTION 🧠
# -----------------------------
def choose_mode(topic, papers, user_mode=None):

    if user_mode in ["fast", "parallel", "research"]:
        return user_mode

    # auto mode
    if len(topic.split()) > 5:
        return "research"

    if len(papers) < 3:
        return "research"

    return "parallel"


# -----------------------------
# ASYNC AGENTS ⚡ (UNCHANGED)
# -----------------------------
async def run_async_agents(topic, top_papers):
    loop = asyncio.get_event_loop()

    summary_task = loop.run_in_executor(None, summarize, topic, top_papers)
    analysis_task = loop.run_in_executor(None, analyze, topic, top_papers)
    sim_task = loop.run_in_executor(None, find_similarities, top_papers)
    gap_task = loop.run_in_executor(None, find_gaps, topic, top_papers)

    return await asyncio.wait_for(
        asyncio.gather(summary_task, analysis_task, sim_task, gap_task),
        timeout=60.0
    )


# -----------------------------
# MAIN PIPELINE
# -----------------------------
async def run_pipeline(topic: str, user_mode: str = None):

    topic = normalize_topic(topic)
    print("🚀 PIPELINE RUNNING")

    emb_model = get_model()

    # -----------------------------
    # FEEDBACK
    # -----------------------------
    feedback = get_feedback(topic)

    if feedback == "bad":
        print("⚠️ Clearing cache due to bad feedback")
        delete_cached_result(topic)

    # -----------------------------
    # CACHE
    # -----------------------------
    cached = get_cached_result(topic)

    if cached and feedback != "bad":
        print("⚡ CACHE HIT (VALID)")
        return cached
    elif cached:
        print("⚠️ Cache ignored due to BAD feedback")

    # -----------------------------
    # QUERY EMBEDDING
    # -----------------------------
    query_embedding = emb_model.encode([topic])[0].astype("float32")

    # -----------------------------
    # FAISS SEARCH
    # -----------------------------
    faiss_results = search_index(query_embedding, k=15)
    faiss_results = deduplicate(faiss_results)
    faiss_results = filter_relevant(faiss_results, topic)

    if is_good_result(faiss_results) and feedback != "bad":
        print("⚡ Using FAISS")

        texts = [p["abstract"][:500] for p in faiss_results]
        embeddings = emb_model.encode(texts)

        top_papers = rerank_hybrid(
            faiss_results,
            topic,
            query_embedding,
            embeddings
        )[:5]

        print("🧠 Extracting insights...")

        for paper in top_papers:
            try:
                insights = extract_insights(paper["abstract"])
                paper["insights"] = insights
            except Exception as e:
                print("⚠️ Insight extraction failed:", str(e))
                paper["insights"] = {
                    "points": [],
                    "keywords": [],
                    "why": "Not available"
                }

    else:
        print("🌐 Fetching fresh data")

        papers = retrieve_papers(topic)

        if not papers or len(papers) < 2:
            print("⚠️ Weak retrieval result")

            return {
                "topic": topic,
                "top_papers": [],
                "summary": "No sufficient research papers found.",
                "analysis": "Try a more specific query.",
                "similarities": [],
                "gaps": [],
                "mode_used": "fallback"
            }

        papers = deduplicate(papers)

        texts = [p["abstract"][:500] for p in papers]
        embeddings = emb_model.encode(texts).astype("float32")

        add_to_index(embeddings, papers)

        faiss_results = search_index(query_embedding, k=15)
        faiss_results = deduplicate(faiss_results)
        faiss_results = filter_relevant(faiss_results, topic)

        texts = [p["abstract"][:500] for p in faiss_results]
        embeddings = emb_model.encode(texts)

        top_papers = rerank_hybrid(
            faiss_results,
            topic,
            query_embedding,
            embeddings
        )[:5]

    # -----------------------------
    # MODE SELECTION
    # -----------------------------
    mode = choose_mode(topic, top_papers, user_mode)
    print(f"⚙️ MODE: {mode}")

    # -----------------------------
    # EXECUTION
    # -----------------------------
    try:
        if mode == "fast":
            from app.agents.llm_combined import generate_full_report

            report = generate_full_report(topic, top_papers)

            summary = report
            analysis = report
            gaps = report
            similarities = find_similarities(top_papers)

        elif mode == "parallel":
            summary, analysis, similarities, gaps = await run_async_agents(topic, top_papers)

        else:  # research mode
            from app.agents.multi_agent import run_multi_agent

            result = await run_multi_agent(topic, top_papers)

            summary = result["summary"]
            analysis = result["analysis"]
            gaps = result["gaps"]
            similarities = find_similarities(top_papers)

    except asyncio.TimeoutError:
        return {"error": "LLM agents timed out. Please try again."}

    # -----------------------------
    # FINAL RESULT
    # -----------------------------
    result = {
        "topic": topic,
        "top_papers": top_papers,
        "summary": summary,
        "analysis": analysis,
        "similarities": similarities,
        "gaps": gaps,
        "mode_used": mode
    }

    # -----------------------------
    # CACHE SAVE
    # -----------------------------
    set_cached_result(topic, result)

    return result