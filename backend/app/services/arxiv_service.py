import requests
import xml.etree.ElementTree as ET

def fetch_arxiv_papers(topic, max_results=5):
    url = f"http://export.arxiv.org/api/query?search_query=all:{topic}&start=0&max_results={max_results}"

    try:
        response = requests.get(url, timeout=10)

        # 🔴 STEP 1: Check status
        if response.status_code != 200:
            print("❌ arXiv API failed:", response.status_code)
            return []

        # 🔴 STEP 2: Check content
        if not response.content or response.content.strip() == b"":
            print("❌ Empty response from arXiv")
            return []

        # 🔴 STEP 3: Safe parse
        try:
            root = ET.fromstring(response.content)
        except ET.ParseError:
            print("❌ Invalid XML from arXiv")
            print("DEBUG:", response.text[:200])
            return []

        papers = []

        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text

            papers.append({
                "title": title.strip(),
                "abstract": summary.strip(),
                "source": "arxiv"
            })

        return papers

    except Exception as e:
        print("❌ arXiv fetch error:", str(e))
        return []