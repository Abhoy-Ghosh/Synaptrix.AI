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

# -----------------------------
# GLOBAL MODEL
# -----------------------------
model = None


def get_model():
    global model
    if model is None:
        print("🔥 Loading embedding model...")
        model = SentenceTransformer('all-mpnet-base-v2', device='cpu')
    return model


# -----------------------------
# DEDUPLICATION (🔥 IMPORTANT)
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

    score = 0
    for word in topic_words:
        if word in text:
            score += 1

    return score / max(len(topic_words), 1)


# -----------------------------
# HYBRID RANKING (OPTIMIZED)
# -----------------------------
def rerank_hybrid(papers, topic, query_embedding, embeddings):

    final_scores = []

    for i, paper in enumerate(papers):
        emb = embeddings[i]

        # Semantic similarity
        semantic = np.dot(emb, query_embedding) / (
            np.linalg.norm(emb) * np.linalg.norm(query_embedding)
        )

        # Keyword match
        keyword = keyword_score(paper["abstract"], topic)

        # Feedback score
        feedback = get_paper_score(paper["title"]) * 0.1

        # Title boost
        title_boost = 0.1 if topic.lower() in paper["title"].lower() else 0

        # Phrase boost
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
# MAIN PIPELINE
# -----------------------------
def run_pipeline(topic: str):

    print("🚀 PIPELINE RUNNING")

    # -----------------------------
    # STEP 0: CACHE
    # -----------------------------
    cached = get_cached_result(topic)
    if cached:
        print("⚡ CACHE HIT")
        return cached

    emb_model = get_model()

    # -----------------------------
    # STEP 1: QUERY EMBEDDING
    # -----------------------------
    query_embedding = emb_model.encode([topic])[0].astype("float32")

    # -----------------------------
    # STEP 2: FEEDBACK
    # -----------------------------
    feedback = get_feedback(topic)

    # -----------------------------
    # STEP 3: FAISS SEARCH
    # -----------------------------
    faiss_results = search_index(query_embedding, k=15)

    # 🔥 DEDUP HERE (VERY IMPORTANT)
    faiss_results = deduplicate(faiss_results)

    if is_good_result(faiss_results) and feedback != "bad":
        print("⚡ Using FAISS memory")

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

        # 🔥 DEDUP BEFORE FAISS INSERT
        papers = deduplicate(papers)

        texts = [p["abstract"][:500] for p in papers]
        embeddings = emb_model.encode(texts).astype("float32")

        # Store in FAISS
        add_to_index(embeddings, papers)

        # Search again
        faiss_results = search_index(query_embedding, k=15)

        # 🔥 DEDUP AGAIN AFTER SEARCH
        faiss_results = deduplicate(faiss_results)

        texts = [p["abstract"][:500] for p in faiss_results]
        embeddings = emb_model.encode(texts)

        top_papers = rerank_hybrid(
            faiss_results,
            topic,
            query_embedding,
            embeddings
        )[:5]

    # -----------------------------
    # STEP 4: AGENTS
    # -----------------------------
    summary = summarize(topic, top_papers)
    analysis = analyze(topic, top_papers)
    similarities = find_similarities(top_papers)
    gaps = find_gaps(topic, top_papers)

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