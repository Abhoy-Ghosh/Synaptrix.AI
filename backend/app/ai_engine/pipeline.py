from app.agents.retriever import retrieve_papers
from app.agents.summarizer import summarize
from app.agents.analyzer import analyze
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

    model = get_model()

    # Cache check
    cached = get_cached_result(topic)
    if cached:
        print("⚡ CACHE HIT")
        return cached

    # Agent 1: Retrieve
    papers = retrieve_papers(topic)

    if not papers:
        return {"error": "No papers found"}

    # Embedding + ranking
    texts = [p["abstract"][:500] for p in papers]
    paper_embeddings = model.encode(texts)
    query_embedding = model.encode([topic])[0]

    scores = np.dot(paper_embeddings, query_embedding) / (
        np.linalg.norm(paper_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    ranked_indices = np.argsort(scores)[::-1]
    top_papers = [papers[i] for i in ranked_indices[:5]]

    # Agent 2: Summarize
    summary = summarize(topic, top_papers)

    # Agent 3: Analyze (🔥 new)
    analysis = analyze(topic, top_papers)

    result = {
        "topic": topic,
        "top_papers": top_papers,
        "summary": summary,
        "analysis": analysis
    }

    set_cached_result(topic, result)

    return result