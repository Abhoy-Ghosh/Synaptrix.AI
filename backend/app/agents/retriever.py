from app.services.semantic_service import fetch_semantic_papers
from app.services.arxiv_service import fetch_arxiv_papers
import time

def load_local_papers():
    import json
    import os

    path = os.path.join(
        os.path.dirname(__file__),
        "../data/sample_papers.json"
    )

    with open(path, "r") as f:
        return json.load(f)
    

def retrieve_papers(topic):
    print("📚 Fetching from Semantic Scholar...")

    s2_papers = []

    # -----------------------------
    # TRY SEMANTIC (SAFE)
    # -----------------------------
    try:
        s2_papers = fetch_semantic_papers(topic, max_results=10)
    except Exception as e:
        print("❌ Semantic Scholar failed:", str(e))

    # -----------------------------
    # RETRY IF EMPTY
    # -----------------------------
    if not s2_papers:
        print("⏳ Retrying Semantic Scholar...")
        time.sleep(2)

        try:
            s2_papers = fetch_semantic_papers(topic, max_results=5)
        except Exception as e:
            print("❌ Retry failed:", str(e))
            s2_papers = []

    # -----------------------------
    # DECIDE ARXIV USAGE
    # -----------------------------
    arxiv_papers = []

    if len(s2_papers) < 3:
        print("⚠️ Weak Semantic results → using arXiv")
        try:
            arxiv_papers = fetch_arxiv_papers(topic, max_results=10)
        except Exception as e:
            print("❌ arXiv failed:", str(e))

    elif len(s2_papers) < 7:
        print("⚡ Augmenting with arXiv")
        try:
            arxiv_papers = fetch_arxiv_papers(topic, max_results=3)
        except Exception as e:
            print("❌ arXiv failed:", str(e))

    # -----------------------------
    # MERGE
    # -----------------------------
    papers = s2_papers + arxiv_papers

    # -----------------------------
    # CLEAN + DEDUP
    # -----------------------------
    cleaned = []
    seen_titles = set()

    for p in papers:
        title = p.get("title", "").strip()
        abstract = p.get("abstract", "").strip()

        if not title or not abstract:
            continue

        key = title.lower()

        if key in seen_titles:
            continue

        seen_titles.add(key)
        cleaned.append(p)

    print(f"✅ Total papers after cleaning: {len(cleaned)}")

    print(f"✅ Total papers after cleaning: {len(cleaned)}")

# 🔥 FINAL FALLBACK
    if len(cleaned) == 0:
        print("⚠️ Using local fallback papers")
        return load_local_papers()

    return cleaned[:10]