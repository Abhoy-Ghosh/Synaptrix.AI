from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def summarize_papers(papers, topic):
    try:
        content = "\n\n".join([
            f"{p['title']}: {p['abstract'][:300]}"
            for p in papers
        ])[:2000]

        prompt = f"""
You are an expert research assistant.

Topic: {topic}

Provide STRICTLY:

1. Key Insights:
- point 1
- point 2

2. Common Themes:
- theme 1
- theme 2

3. Summary:
(3-4 lines)

Papers:
{content}
"""

        response = client.models.generate_content(
            model="models/gemini-1.5-flash",  # ✅ FIXED
            contents=prompt
        )

        return response.text if response.text else "No summary generated"

    except Exception as e:
        return f"LLM Error: {str(e)}"