from sentence_transformers import SentenceTransformer
from app.services.arxiv_service import fetch_arxiv_papers
from app.services.llm_service import summarize_papers
from app.cache.cache import get_cached_result, set_cached_result
import numpy as np

model = None


def get_model():
    global model
    if model is None:
        print("🔥 Loading embedding model (first time)...")
        model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    return model


def run_pipeline(topic: str):

    model = get_model()

    # Step 0: Check cache
    cached = get_cached_result(topic)
    if cached:
        print("⚡ CACHE HIT")
        return cached

    # Step 1: Fetch papers
    papers = fetch_arxiv_papers(topic, max_results=5)

    if not papers:
        return {"error": "No papers found"}

    # Step 2: embeddings
    texts = [p["abstract"][:500] for p in papers]
    paper_embeddings = model.encode(texts)

    # Step 3: query embedding
    query_embedding = model.encode([topic])[0]

    # Step 4: cosine similarity
    scores = np.dot(paper_embeddings, query_embedding) / (
        np.linalg.norm(paper_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    # Step 5: rank papers
    ranked_indices = np.argsort(scores)[::-1]
    top_papers = [papers[i] for i in ranked_indices[:5]]

    # Step 6: summarize
    summary = summarize_papers(top_papers, topic)

    # Step 7: prepare result
    result = {
        "topic": topic,
        "top_papers": top_papers,
        "summary": summary
    }

    # Step 8: cache result
    set_cached_result(topic, result)

    return result