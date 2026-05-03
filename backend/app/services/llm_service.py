from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"


def summarize_papers(papers, topic):
    try:
        content = "\n\n".join([
            f"{p['title']}: {p['abstract'][:300]}"
            for p in papers
        ])[:2000]

        prompt = f"""
Topic: {topic}

Give:
1. Key insights
2. Common themes
3. Short summary

Papers:
{content}
"""
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text if response.text else "No summary generated"

    except Exception as e:
        return f"LLM Error: {str(e)}"