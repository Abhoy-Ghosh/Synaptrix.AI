from sentence_transformers import SentenceTransformer
from app.services.arxiv_service import fetch_arxiv_papers
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')


def run_pipeline(topic: str):

    # Step 1: Fetch papers
    papers = fetch_arxiv_papers(topic, max_results=10)

    if not papers:
        return {"error": "No papers found"}

    # Step 2: embeddings
    texts = [p["abstract"] for p in papers]
    paper_embeddings = model.encode(texts)

    # Step 3: query embedding
    query_embedding = model.encode([topic])[0]

    # Step 4: cosine similarity
    scores = np.dot(paper_embeddings, query_embedding)

    # Step 5: rank papers
    ranked_indices = np.argsort(scores)[::-1]

    top_papers = [papers[i] for i in ranked_indices[:5]]

    return {
        "topic": topic,
        "top_papers": top_papers
    }