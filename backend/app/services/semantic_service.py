import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def fetch_semantic_papers(query, max_results=5, retry=2):
    print("📚 Fetching from Semantic Scholar...")

    if not API_KEY:
        print("❌ Missing Semantic Scholar API key")
        return []

    headers = {
        "x-api-key": API_KEY
    }

    params = {
        "query": query,
        "limit": max_results,
        "fields": "title,abstract,year,citationCount"
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)

        # 🔁 Handle rate limit
        if response.status_code == 429 and retry > 0:
            print("⏳ Rate limited. Retrying...")
            time.sleep(2)
            return fetch_semantic_papers(query, max_results, retry - 1)

        # ❌ Any other error
        if response.status_code != 200:
            print("❌ Semantic Scholar API error:", response.status_code)
            return []

        data = response.json()

        papers = []

        for paper in data.get("data", []):
            title = paper.get("title")
            abstract = paper.get("abstract")

            # Skip bad entries
            if not title or not abstract:
                continue

            papers.append({
                "title": title.strip(),
                "abstract": abstract.strip(),
                "year": paper.get("year", 2020),
                "citations": paper.get("citationCount", 0),
                "source": "semantic"
            })

        print(f"✅ Semantic Scholar returned {len(papers)} papers")

        return papers

    except Exception as e:
        print("❌ Semantic Scholar fetch error:", str(e))
        return []