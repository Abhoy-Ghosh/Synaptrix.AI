from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ SAFE MODEL (works with your SDK)
model = genai.GenerativeModel("gemini-pro")


def summarize_papers(papers, topic):
    try:
        # Limit input size (VERY IMPORTANT)
        content = "\n\n".join([
            f"Title: {p['title']}\nAbstract: {p['abstract'][:300]}"
            for p in papers
        ])[:2000]

        prompt = f"""
You are a research assistant.

Topic: {topic}

Give:
- Key insights
- Main themes
- Short summary

Papers:
{content}
"""

        response = model.generate_content(prompt)

        return response.text if response.text else "No summary generated"

    except Exception as e:
        return f"LLM Error: {str(e)}"