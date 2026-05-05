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
# MODEL (LAZY LOAD)
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
    return [
        p for p in papers
        if any(w in p.get("abstract", "").lower() for w in topic_words)
    ]


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

    if len(topic.split()) > 5 or len(papers) < 3:
        return "research"

    return "parallel"


# -----------------------------
# PARALLEL MODE (SAFE)
# -----------------------------
async def run_parallel(topic, papers):
    print("⚡ Parallel mode")

    loop = asyncio.get_running_loop()

    summary_task = loop.run_in_executor(None, summarize, topic, papers)
    analysis_task = loop.run_in_executor(None, analyze, topic, papers)
    gaps_task = loop.run_in_executor(None, find_gaps, topic, papers)

    results = await asyncio.gather(
        summary_task,
        analysis_task,
        gaps_task,
        return_exceptions=True
    )

    summary, analysis, gaps = results

    if isinstance(summary, Exception):
        print("⚠️ Summary failed:", summary)
        summary = "Summary not available"

    if isinstance(analysis, Exception):
        print("⚠️ Analysis failed:", analysis)
        analysis = "Analysis not available"

    if isinstance(gaps, Exception):
        print("⚠️ Gaps failed:", gaps)
        gaps = "Gap analysis not available"

    return summary, analysis, gaps


# -----------------------------
# SEQUENTIAL MODE (SAFE)
# -----------------------------
def _safe(text, fallback):
    if not text or len(str(text).strip()) < 20:
        return fallback
    return text


async def run_sequential(topic, papers):
    print("🧠 Sequential reasoning mode")

    summary = summarize(topic, papers)
    summary = _safe(summary, "Summary not available")

    analysis = analyze(
        f"{topic}\n\nSummary:\n{summary}",
        papers
    )
    analysis = _safe(analysis, "Analysis not available")

    gaps = find_gaps(
        f"{topic}\n\nSummary:\n{summary}\n\nAnalysis:\n{analysis}",
        papers
    )
    gaps = _safe(gaps, "Gap analysis not available")

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
    # SEARCH (FAISS)
    # -----------------------------
    faiss_results = search_index(query_embedding, k=15)
    faiss_results = deduplicate(faiss_results)
    faiss_results = filter_relevant(faiss_results, topic)

    if len(faiss_results) < 3:
        print("🌐 Fetching fresh data")

        papers = retrieve_papers(topic)
        if not papers:
            return {"error": "No papers found"}

        papers = deduplicate(papers)

        embeddings = emb_model.encode([p["abstract"] for p in papers])
        add_to_index(embeddings, papers)

        faiss_results = search_index(query_embedding, k=15)

    # -----------------------------
    # RANK
    # -----------------------------
    embeddings = emb_model.encode([p["abstract"] for p in faiss_results])
    top_papers = rerank_hybrid(
        faiss_results, topic, query_embedding, embeddings
    )[:5]

    # -----------------------------
    # INSIGHTS (ALWAYS)
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
    # FINAL OUTPUT
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