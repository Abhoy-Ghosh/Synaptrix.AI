from app.agents.retriever import retrieve_papers
from app.agents.summarizer import summarize
from app.agents.analyzer import analyze
from app.agents.similarity import find_similarities
from app.agents.gap_finder import find_gaps
from app.cache.cache import get_cached_result, set_cached_result
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

    # Step 0: Cache check FIRST
    cached = get_cached_result(topic)
    if cached:
        print("⚡ CACHE HIT")
        return cached

    # Step 1: Load model only if needed
    emb_model = get_model()

    # Step 2: Retrieve
    papers = retrieve_papers(topic)

    if not papers:
        return {"error": "No papers found"}

    # Step 3: Embedding + ranking
    texts = [p["abstract"][:500] for p in papers]
    paper_embeddings = emb_model.encode(texts)
    query_embedding = emb_model.encode([topic])[0]

    scores = np.dot(paper_embeddings, query_embedding) / (
        np.linalg.norm(paper_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    ranked_indices = np.argsort(scores)[::-1]
    top_papers = [papers[i] for i in ranked_indices[:5]]

    # Step 4: Agents
    summary = summarize(topic, top_papers)
    analysis = analyze(topic, top_papers)
    similarities = find_similarities(top_papers)
    gaps = find_gaps(topic, top_papers)

    # Step 5: Final result (FIXED)
    result = {
        "topic": topic,
        "top_papers": top_papers,
        "summary": summary,
        "analysis": analysis,
        "similarities": similarities,
        "gaps": gaps
    }

    # Step 6: Cache full result
    set_cached_result(topic, result)

    return result