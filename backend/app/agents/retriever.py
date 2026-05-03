from app.services.arxiv_service import fetch_arxiv_papers

def retrieve_papers(topic):
    print("🤖 Retriever Agent working...")
    return fetch_arxiv_papers(topic, max_results=5)