from app.services.semantic_service import fetch_semantic_papers
from app.services.arxiv_service import fetch_arxiv_papers
import time


def retrieve_papers(topic):
    print("📚 Fetching from Semantic Scholar...")

    # -----------------------------
    # TRY SEMANTIC WITH RETRY
    # -----------------------------
    s2_papers = fetch_semantic_papers(topic, max_results=10)

    if not s2_papers:
        print("⏳ Retry Semantic Scholar...")
        time.sleep(2)
        s2_papers = fetch_semantic_papers(topic, max_results=5)

    # -----------------------------
    # FALLBACK TO ARXIV
    # -----------------------------
    if len(s2_papers) < 3:
        print("⚠️ Weak Semantic results → using arXiv")
        arxiv_papers = fetch_arxiv_papers(topic, max_results=7)
    else:
        arxiv_papers = fetch_arxiv_papers(topic, max_results=3)

    # -----------------------------
    # MERGE
    # -----------------------------
    papers = s2_papers + arxiv_papers

    # -----------------------------
    # FILTER BAD PAPERS
    # -----------------------------
    cleaned = []
    seen_titles = set()

    for p in papers:
        title = p.get("title", "").strip()
        abstract = p.get("abstract", "").strip()

        if not title or not abstract:
            continue

        # deduplicate
        if title.lower() in seen_titles:
            continue

        seen_titles.add(title.lower())
        cleaned.append(p)

    print(f"✅ Total papers after cleaning: {len(cleaned)}")

    return cleaned[:10]