from app.services.llm_service import summarize_papers

def summarize(topic, papers):
    print("🤖 Summarizer Agent working...")
    return summarize_papers(papers, topic)