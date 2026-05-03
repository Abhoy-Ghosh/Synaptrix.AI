from app.agents.retriever import retrieve_papers
from app.agents.summarizer import summarize
from app.agents.analyzer import analyze
from app.agents.similarity import find_similarities
from app.agents.gap_finder import find_gaps
from app.cache.cache import get_cached_result, set_cached_result
from app.retrieval.vector_store import add_to_index, search_index

from sentence_transformers import SentenceTransformer
import numpy as np

model = None


def get_model():
    global model
    if model is None:
        print("🔥 Loading embedding model...")
        model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    return model


def run_pipeline(topic: str):

    print("🚀 PIPELINE RUNNING")

    # -----------------------------
    # STEP 0: CACHE CHECK
    # -----------------------------
    cached = get_cached_result(topic)
    if cached:
        print("⚡ CACHE HIT")
        return cached

    # -----------------------------
    # STEP 1: LOAD MODEL
    # -----------------------------
    emb_model = get_model()

    # -----------------------------
    # STEP 2: RETRIEVE PAPERS
    # -----------------------------
    papers = retrieve_papers(topic)

    if not papers:
        return {"error": "No papers found"}

    # -----------------------------
    # STEP 3: EMBEDDINGS
    # -----------------------------
    texts = [p["abstract"][:500] for p in papers]
    paper_embeddings = emb_model.encode(texts).astype("float32")

    # -----------------------------
    # STEP 4: STORE IN FAISS
    # -----------------------------
    add_to_index(paper_embeddings, papers)
    print(f"📦 Stored {len(papers)} papers in FAISS")

    # -----------------------------
    # STEP 5: QUERY EMBEDDING
    # -----------------------------
    query_embedding = emb_model.encode([topic])[0].astype("float32")

    # -----------------------------
    # STEP 6: SEARCH FROM FAISS
    # -----------------------------
    top_papers = search_index(query_embedding, k=5)

    # -----------------------------
    # STEP 7: MULTI-AGENT PROCESSING
    # -----------------------------
    summary = summarize(topic, top_papers)
    analysis = analyze(topic, top_papers)
    similarities = find_similarities(top_papers)
    gaps = find_gaps(topic, top_papers)

    # -----------------------------
    # STEP 8: FINAL RESPONSE
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
    # STEP 9: CACHE RESULT
    # -----------------------------
    set_cached_result(topic, result)

    return result