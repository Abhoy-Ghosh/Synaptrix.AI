import requests


def fetch_semantic_papers(query, limit=10):

    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,abstract,year,citationCount"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            print("❌ Semantic Scholar API error:", response.status_code)
            return []

        data = response.json()

        papers = []

        for p in data.get("data", []):
            papers.append({
                "title": p.get("title", ""),
                "abstract": p.get("abstract", "") or "",
                "year": p.get("year", 0),
                "citations": p.get("citationCount", 0),
                "source": "semantic"
            })

        return papers

    except Exception as e:
        print("❌ Semantic Scholar fetch error:", str(e))
        return []