from app.services.semantic_service import fetch_semantic_papers
from app.services.arxiv_service import fetch_arxiv_papers


def retrieve_papers(topic):

    print("📚 Fetching from Semantic Scholar...")
    s2_papers = fetch_semantic_papers(topic, limit=10)

    # fallback condition
    if len(s2_papers) < 5:
        print("⚠️ Weak Semantic Scholar results → fallback to arXiv")
        arxiv_papers = fetch_arxiv_papers(topic, max_results=5)
    else:
        arxiv_papers = []

    # merge
    papers = s2_papers + arxiv_papers

    return papers