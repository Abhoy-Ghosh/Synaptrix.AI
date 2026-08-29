from app.services.semantic_service import (
    fetch_semantic_papers
)

from app.services.arxiv_service import (
    fetch_arxiv_papers
)

from app.services.ieee_service import (
    fetch_ieee_papers
)

from app.services.springer_service import (
    fetch_springer_papers
)

import time
import json
import os


# =========================================
# LOCAL FALLBACK
# =========================================

def load_local_papers():

    path = os.path.join(

        os.path.dirname(__file__),

        "../data/sample_papers.json"
    )

    with open(path, "r") as f:

        return json.load(f)


# =========================================
# CLEAN + DEDUP
# =========================================

def clean_papers(papers):

    cleaned = []

    seen_titles = set()

    for p in papers:

        title = p.get(
            "title",
            ""
        ).strip()

        abstract = p.get(
            "abstract",
            ""
        ).strip()

        if not title or not abstract:
            continue

        key = title.lower()

        if key in seen_titles:
            continue

        seen_titles.add(key)

        cleaned.append(p)

    return cleaned


# =========================================
# RETRIEVER
# =========================================

def retrieve_papers(topic):

    print("🌐 Multi-source retrieval started")

    papers = []

    # =====================================
    # SEMANTIC SCHOLAR
    # =====================================

    semantic_papers = []

    try:

        semantic_papers = fetch_semantic_papers(

            topic,

            max_results=10
        )

    except Exception as e:

        print(
            "❌ Semantic Scholar failed:",
            str(e)
        )

    papers.extend(semantic_papers)

    # =====================================
    # IEEE
    # =====================================

    ieee_papers = []

    try:

        ieee_papers = fetch_ieee_papers(

            topic,

            max_results=5
        )

    except Exception as e:

        print(
            "❌ IEEE failed:",
            str(e)
        )

    papers.extend(ieee_papers)

    # =====================================
    # SPRINGER
    # =====================================

    springer_papers = []

    try:

        springer_papers = fetch_springer_papers(

            topic,

            max_results=5
        )

    except Exception as e:

        print(
            "❌ Springer failed:",
            str(e)
        )

    papers.extend(springer_papers)

    # =====================================
    # arXiv FALLBACK
    # =====================================

    arxiv_papers = []

    if len(papers) < 5:

        print(
            "⚠️ Weak retrieval → using arXiv fallback"
        )

        time.sleep(1)

        try:

            arxiv_papers = fetch_arxiv_papers(

                topic,

                max_results=7
            )

        except Exception as e:

            print(
                "❌ arXiv failed:",
                str(e)
            )

    elif len(papers) < 10:

        print(
            "⚡ Augmenting with arXiv"
        )

        try:

            arxiv_papers = fetch_arxiv_papers(

                topic,

                max_results=3
            )

        except Exception as e:

            print(
                "❌ arXiv failed:",
                str(e)
            )

    papers.extend(arxiv_papers)

    # =====================================
    # CLEAN
    # =====================================

    cleaned = clean_papers(papers)

    print(
        f"✅ Total papers after cleaning: "
        f"{len(cleaned)}"
    )

    # =====================================
    # LOCAL FALLBACK
    # =====================================

    if len(cleaned) == 0:

        print(
            "⚠️ Using local fallback papers"
        )

        return load_local_papers()

    # =====================================
    # FINAL LIMIT
    # =====================================

    return cleaned[:15]