import asyncio
import time
import numpy as np
from sentence_transformers import SentenceTransformer

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


# -----------------------------
# NORMALIZE
# -----------------------------
def normalize_topic(topic):
    return topic.strip().lower()


# -----------------------------
# MODEL
# -----------------------------
_model = None

def get_model():
    global _model
    if _model is None:
        print("🔥 Loading embedding model...")
        start = time.time()
        _model = SentenceTransformer('all-mpnet-base-v2')
        print("Model load time:", time.time() - start)
    return _model


def warmup_model():
    get_model()
    print("✅ Embedding model warm")


# -----------------------------
# HELPERS
# -----------------------------
def deduplicate(papers):
    seen = set()
    unique = []
    for p in papers:
        title = p.get("title", "").lower()
        if title and title not in seen:
            seen.add(title)
            unique.append(p)
    return unique


def filter_relevant(papers, topic):
    topic_words = topic.lower().split()
    filtered = []

    for p in papers:
        text = (p.get("title","") + " " + p.get("abstract","")).lower()
        match_count = sum(1 for w in topic_words if w in text)

        if match_count >= max(1, len(topic_words)//2):
            filtered.append(p)

    return filtered


def keyword_score(text, topic):
    text = text.lower()
    topic_words = topic.lower().split()
    score = sum(1 for w in topic_words if w in text)
    return score / max(len(topic_words), 1)


def safe_text(x, fallback="Not available"):
    if not x or len(str(x).strip()) < 5:
        return fallback
    return x


# -----------------------------
# HYBRID RANKING
# -----------------------------
def rerank_hybrid(papers, topic, query_embedding, embeddings):
    scores = []

    for i, paper in enumerate(papers):
        emb = embeddings[i]

        semantic = np.dot(emb, query_embedding) / (
            np.linalg.norm(emb) * np.linalg.norm(query_embedding)
        )

        keyword = keyword_score(paper["abstract"], topic)
        feedback = min(get_paper_score(paper["title"]), 1.0) * 0.15
        citation = min(paper.get("citations", 0) / 1000, 1.0) * 0.1

        final = 0.6 * semantic + 0.25 * keyword + feedback + citation

        scores.append((final, paper))

    scores.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scores]


# -----------------------------
# MODE SELECTION
# -----------------------------
def choose_mode(topic, papers, user_mode=None):
    if user_mode in ["fast", "parallel", "research"]:
        return user_mode

    if len(papers) < 3:
        return "fast"

    if len(topic.split()) > 5:
        return "research"

    return "parallel"


# -----------------------------
# PARALLEL MODE
# -----------------------------
async def run_parallel(topic, papers):
    print("⚡ Parallel mode")

    loop = asyncio.get_running_loop()

    summary_task = loop.run_in_executor(None, summarize, topic, papers)
    analysis_task = loop.run_in_executor(None, analyze, topic, papers)
    gaps_task = loop.run_in_executor(None, find_gaps, topic, papers)

    summary, analysis, gaps = await asyncio.gather(
        summary_task,
        analysis_task,
        gaps_task,
        return_exceptions=True
    )

    if isinstance(summary, Exception):
        summary = "Summary not available"

    if isinstance(analysis, Exception):
        analysis = "Analysis not available"

    if isinstance(gaps, Exception):
        gaps = "Gap analysis not available"

    return summary, analysis, gaps


# -----------------------------
# SEQUENTIAL MODE
# -----------------------------
async def run_sequential(topic, papers):
    print("🧠 Sequential research mode")

    summary = safe_text(summarize(topic, papers))

    analysis = safe_text(
        analyze(f"{topic}\n\nSummary:\n{summary}", papers)
    )

    gaps = safe_text(
        find_gaps(f"{topic}\n\nSummary:\n{summary}\n\nAnalysis:\n{analysis}", papers)
    )

    return summary, analysis, gaps


# -----------------------------
# MAIN PIPELINE
# -----------------------------
async def run_pipeline(topic: str, user_mode: str = None):

    topic = normalize_topic(topic)
    print("🚀 PIPELINE RUNNING")

    emb_model = get_model()

    # -----------------------------
    # CACHE
    # -----------------------------
    feedback = get_feedback(topic)

    if feedback == "bad":
        delete_cached_result(topic)

    cached = get_cached_result(topic, user_mode)

    if cached and feedback != "bad":
        print("⚡ CACHE HIT")
        return cached

    # -----------------------------
    # EMBEDDING
    # -----------------------------
    query_embedding = emb_model.encode([topic])[0]

    # -----------------------------
    # FAISS SEARCH
    # -----------------------------
    faiss_results = search_index(query_embedding, k=15)
    faiss_results = deduplicate(faiss_results)
    faiss_results = filter_relevant(faiss_results, topic)

    # -----------------------------
    # FETCH IF NEEDED
    # -----------------------------
    if len(faiss_results) < 3:
        print("🌐 Fetching fresh data")

        papers = retrieve_papers(topic)
        papers = deduplicate(papers)

        if papers:
            embeddings = emb_model.encode([p["abstract"] for p in papers])
            add_to_index(embeddings, papers)

            faiss_results = search_index(query_embedding, k=15)
            faiss_results = filter_relevant(faiss_results, topic)

    # -----------------------------
    # RANK
    # -----------------------------
    if not faiss_results:
        print("⚠️ No strong FAISS results, continuing with fallback papers")
        faiss_results = papers if 'papers' in locals() else []

    embeddings = emb_model.encode([p["abstract"] for p in faiss_results]) if faiss_results else []

    top_papers = rerank_hybrid(
        faiss_results, topic, query_embedding, embeddings
    )[:5] if faiss_results else []

    print("DEBUG: top_papers count =", len(top_papers))

    # -----------------------------
    # INSIGHTS (ALWAYS RUN)
    # -----------------------------
    print("🧠 Extracting insights...")

    for p in top_papers:
        p["insights"] = extract_insights(p.get("abstract", ""))

    # -----------------------------
    # MODE
    # -----------------------------
    mode = choose_mode(topic, top_papers, user_mode)
    print("⚙️ MODE:", mode)

    # -----------------------------
    # EXECUTION
    # -----------------------------
    if mode == "fast":
        from app.agents.llm_combined import generate_full_report

        report = generate_full_report(topic, top_papers)

        summary = report
        analysis = "Included in summary"
        gaps = "Included in summary"

    elif mode == "parallel":
        summary, analysis, gaps = await run_parallel(topic, top_papers)

    else:
        summary, analysis, gaps = await run_sequential(topic, top_papers)

    similarities = find_similarities(top_papers)

    # -----------------------------
    # OUTPUT
    # -----------------------------
    result = {
        "topic": topic,
        "top_papers": top_papers,
        "summary": safe_text(summary),
        "analysis": safe_text(analysis),
        "gaps": safe_text(gaps),
        "similarities": similarities,
        "mode_used": mode
    }

    set_cached_result(topic, mode, result)

    return result