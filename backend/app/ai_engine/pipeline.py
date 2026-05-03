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

model = None


def get_model():
    global model
    if model is None:
        print("🔥 Loading embedding model...")
        model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    return model


def is_good_result(results):
    return len(results) >= 3


def rerank_with_feedback(papers, query_embedding, model):
    texts = [p["abstract"][:500] for p in papers]
    embeddings = model.encode(texts)

    final_scores = []

    for i, paper in enumerate(papers):
        emb = embeddings[i]

        # semantic score
        semantic = np.dot(emb, query_embedding) / (
            np.linalg.norm(emb) * np.linalg.norm(query_embedding)
        )

        # feedback score
        feedback_score = get_paper_score(paper["title"]) * 0.2

        final = semantic + feedback_score

        final_scores.append((final, paper))

    final_scores.sort(key=lambda x: x[0], reverse=True)

    return [p for _, p in final_scores]


def run_pipeline(topic: str):

    print("🚀 PIPELINE RUNNING")

    # ---------------- CACHE ----------------
    cached = get_cached_result(topic)
    if cached:
        print("⚡ CACHE HIT")
        return cached

    emb_model = get_model()

    # ---------------- QUERY EMB ----------------
    query_embedding = emb_model.encode([topic])[0]

    # ---------------- FEEDBACK ----------------
    feedback = get_feedback(topic)

    # ---------------- FAISS SEARCH ----------------
    faiss_results = search_index(query_embedding, k=10)

    if is_good_result(faiss_results) and feedback != "bad":
        print("⚡ Using FAISS")

        top_papers = rerank_with_feedback(
            faiss_results, query_embedding, emb_model
        )[:5]

    else:
        print("🌐 Fetching fresh data")

        papers = retrieve_papers(topic)

        if not papers:
            return {"error": "No papers found"}

        texts = [p["abstract"][:500] for p in papers]
        embeddings = emb_model.encode(texts).astype("float32")

        add_to_index(embeddings, papers)

        faiss_results = search_index(query_embedding, k=10)

        top_papers = rerank_with_feedback(
            faiss_results, query_embedding, emb_model
        )[:5]

    # ---------------- AGENTS ----------------
    summary = summarize(topic, top_papers)
    analysis = analyze(topic, top_papers)
    similarities = find_similarities(top_papers)
    gaps = find_gaps(topic, top_papers)

    # ---------------- RESULT ----------------
    result = {
        "topic": topic,
        "top_papers": top_papers,
        "summary": summary,
        "analysis": analysis,
        "similarities": similarities,
        "gaps": gaps
    }

    set_cached_result(topic, result)

    return result