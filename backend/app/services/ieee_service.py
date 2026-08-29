import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

IEEE_API_KEY = os.getenv("IEEE_API_KEY")

BASE_URL = (
    "https://ieeexploreapi.ieee.org/api/v1/search/articles"
)


def fetch_ieee_papers(

    query,
    max_results=5,
    retry=3

):

    print("📘 Fetching from IEEE Xplore...")

    if not IEEE_API_KEY:

        print("❌ Missing IEEE API key")

        return []

    params = {

        "apikey": IEEE_API_KEY,

        "format": "json",

        "querytext": query,

        "max_records": max_results
    }

    for attempt in range(retry):

        try:

            response = requests.get(

                BASE_URL,

                params=params,

                timeout=20
            )

            if response.status_code == 429:

                print(
                    f"⏳ IEEE rate limited "
                    f"(Attempt {attempt+1}/{retry})"
                )

                time.sleep(2)

                continue

            if response.status_code != 200:

                print(
                    "❌ IEEE API error:",
                    response.status_code
                )

                return []

            data = response.json()

            articles = data.get(
                "articles",
                []
            )

            papers = []

            for article in articles:

                title = article.get(
                    "title",
                    ""
                ).strip()

                abstract = article.get(
                    "abstract",
                    ""
                ).strip()

                if not title or not abstract:
                    continue

                papers.append({

                    "title": title,

                    "abstract": abstract,

                    "year": article.get(
                        "publication_year",
                        2020
                    ),

                    "citations": article.get(
                        "citing_paper_count",
                        0
                    ),

                    "source": "ieee"
                })

            print(
                f"✅ IEEE returned "
                f"{len(papers)} papers"
            )

            return papers

        except Exception as e:

            print(
                "❌ IEEE fetch error:",
                str(e)
            )

            time.sleep(2)

    print("❌ IEEE failed after retries")

    return []