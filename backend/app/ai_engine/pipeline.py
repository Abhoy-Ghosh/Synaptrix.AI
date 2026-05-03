from app.agents.retriever import retrieve_papers
from app.agents.summarizer import summarize
from app.agents.analyzer import analyze
from app.agents.similarity import find_similarities
from app.agents.gap_finder import find_gaps

from app.cache.cache import get_cached_result, set_cached_result
from app.retrieval.vector_store import add_to_index, search_index
from app.feedback.feedback_store import get_feedback
from app.feedback.paper_feedback import get_paper_score

from sentence_transformers import SentenceTransformer
import numpy as np
import asyncio

def normalize_topic(topic):
    return topic.strip().lower()

model = None


# -----------------------------
# MODEL
# -----------------------------
def get_model():
    global model
    if model is None:
        print("🔥 Loading embedding model...")
        model = SentenceTransformer('all-mpnet-base-v2', device='cpu')
    return model


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
# FILER RELAVANT PAPERS
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
        feedback = get_paper_score(paper["title"]) * 0.5
        title_boost = 0.1 if topic.lower() in paper["title"].lower() else 0
        phrase_boost = 0.1 if topic.lower() in paper["abstract"].lower() else 0

        final = (
            0.6 * semantic +
            0.25 * keyword +
            0.15 * feedback +
            title_boost +
            phrase_boost
        )

        final_scores.append((final, paper))

    final_scores.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in final_scores]


# -----------------------------
# ASYNC AGENTS
# -----------------------------
async def run_async_agents(topic, top_papers):
    loop = asyncio.get_event_loop()

    summary_task = loop.run_in_executor(None, summarize, topic, top_papers)
    analysis_task = loop.run_in_executor(None, analyze, topic, top_papers)
    sim_task = loop.run_in_executor(None, find_similarities, top_papers)
    gap_task = loop.run_in_executor(None, find_gaps, topic, top_papers)

    return await asyncio.gather(
        summary_task,
        analysis_task,
        sim_task,
        gap_task
    )


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def run_pipeline(topic: str):

    topic = normalize_topic(topic)

    print("🚀 PIPELINE RUNNING")

    emb_model = get_model()

    # -----------------------------
    # STEP 0: FEEDBACK FIRST 
    # -----------------------------
    feedback = get_feedback(topic)

    # CLEAR CACHE ON BAD FEEDBACK
    if feedback == "bad":
        print("⚠️ Clearing cache due to bad feedback")
        set_cached_result(topic, None)    

    # -----------------------------
    # STEP 1: CACHE (SMART)
    # -----------------------------
    cached = get_cached_result(topic)

    if cached and feedback != "bad":
        print("⚡ CACHE HIT (VALID)")
        return cached
    elif cached:
        print("⚠️ Cache ignored due to BAD feedback")

    # -----------------------------
    # STEP 2: QUERY EMBEDDING
    # -----------------------------
    query_embedding = emb_model.encode([topic])[0].astype("float32")

    # -----------------------------
    # STEP 3: FAISS
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

    else:
        print("🌐 Fetching fresh data")

        papers = retrieve_papers(topic)
        if not papers:
            return {"error": "No papers found"}

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
    # STEP 4: ASYNC AGENTS ⚡
    # -----------------------------
    summary, analysis, similarities, gaps = asyncio.run(
        run_async_agents(topic, top_papers)
    )

    # -----------------------------
    # STEP 5: RESULT
    # -----------------------------
    result = {
        "topic": topic,
        "top_papers": top_papers,
        "summary": summary,
        "analysis": analysis,
        "similarities": similarities,
        "gaps": gaps
    }

    # -----------------------------
    # STEP 6: CACHE
    # -----------------------------
    set_cached_result(topic, result)

    return result