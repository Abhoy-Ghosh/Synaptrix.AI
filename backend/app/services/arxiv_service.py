import requests
import xml.etree.ElementTree as ET
import time

def fetch_arxiv_papers(query: str, max_results: int = 5):

    time.sleep(1)  # ✅ avoid rate limit

    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    
    response = requests.get(url)
    root = ET.fromstring(response.content)

    papers = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text

        papers.append({
            "title": title.strip(),
            "abstract": summary.strip()
        })

    return papers