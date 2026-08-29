import time
import requests
import xml.etree.ElementTree as ET


ARXIV_BASE_URL = (
    "https://export.arxiv.org/api/query"
)


HEADERS = {
    "User-Agent":
    "SynaptrixAI/1.0 (Research Intelligence Engine)"
}


def fetch_arxiv_papers(

    topic,
    max_results=5,
    retry=3

):

    print("📚 Fetching from arXiv...")

    url = (

        f"{ARXIV_BASE_URL}"

        f"?search_query=all:{topic}"

        f"&start=0"

        f"&max_results={max_results}"
    )

    for attempt in range(retry):

        try:

            response = requests.get(

                url,

                headers=HEADERS,

                timeout=30
            )

            # =====================================
            # RATE LIMIT
            # =====================================

            if response.status_code == 429:

                print(
                    f"⏳ arXiv rate limited "
                    f"(Attempt {attempt+1}/{retry})"
                )

                time.sleep(2)

                continue

            # =====================================
            # STATUS CHECK
            # =====================================

            if response.status_code != 200:

                print(
                    "❌ arXiv API failed:",
                    response.status_code
                )

                return []

            # =====================================
            # EMPTY RESPONSE
            # =====================================

            if not response.content:

                print("❌ Empty response from arXiv")

                return []

            # =====================================
            # SAFE XML PARSE
            # =====================================

            try:

                root = ET.fromstring(
                    response.content
                )

            except ET.ParseError:

                print("❌ Invalid XML from arXiv")

                print(
                    "DEBUG:",
                    response.text[:200]
                )

                return []

            # =====================================
            # PARSE PAPERS
            # =====================================

            papers = []

            for entry in root.findall(
                "{http://www.w3.org/2005/Atom}entry"
            ):

                title_elem = entry.find(
                    "{http://www.w3.org/2005/Atom}title"
                )

                summary_elem = entry.find(
                    "{http://www.w3.org/2005/Atom}summary"
                )

                if (
                    title_elem is None
                    or summary_elem is None
                ):
                    continue

                title = (
                    title_elem.text or ""
                ).strip()

                summary = (
                    summary_elem.text or ""
                ).strip()

                # Skip weak papers
                if not title or not summary:
                    continue

                papers.append({

                    "title": title,

                    "abstract": summary,

                    "source": "arxiv"
                })

            print(
                f"✅ arXiv returned "
                f"{len(papers)} papers"
            )

            return papers

        except requests.Timeout:

            print(
                f"⏳ arXiv timeout "
                f"(Attempt {attempt+1}/{retry})"
            )

            time.sleep(2)

        except requests.RequestException as e:

            print(
                "❌ arXiv request error:",
                str(e)
            )

            time.sleep(2)

        except Exception as e:

            print(
                "❌ arXiv unexpected error:",
                str(e)
            )

            return []

    print("❌ arXiv failed after retries")

    return []