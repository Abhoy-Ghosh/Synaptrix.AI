from app.agents.retriever import retrieve_papers
from app.agents.summarizer import summarize
from app.agents.analyzer import analyze
from app.agents.similarity import find_similarities
from app.agents.gap_finder import find_gaps
from app.cache.cache import get_cached_result, set_cached_result
from app.retrieval.vector_store import add_to_index, search_index
from app.feedback.feedback_store import get_feedback

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
    # STEP 2: CHECK FEEDBACK
    # -----------------------------
    feedback = get_feedback(topic)

    # -----------------------------
    # STEP 3: FAISS SEARCH FIRST
    # -----------------------------
    faiss_results = search_index(query_embedding, k=5)

    if is_good_result(faiss_results) and feedback != "bad":
        print("⚡ Using FAISS results")
        top_papers = faiss_results

    else:
        print("🌐 Fetching from API (low FAISS quality or bad feedback)")

        papers = retrieve_papers(topic)

        if not papers:
            return {"error": "No papers found"}

        texts = [p["abstract"][:500] for p in papers]
        paper_embeddings = emb_model.encode(texts).astype("float32")

        # Store in FAISS
        add_to_index(paper_embeddings, papers)

        # Search again
        top_papers = search_index(query_embedding, k=5)

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

    return resultgot