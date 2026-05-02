from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()  # load .env

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")


def summarize_papers(papers, topic):

    content = "\n\n".join([
        f"Title: {p['title']}\nAbstract: {p['abstract']}"
        for p in papers
    ])

    prompt = f"""
You are an expert research assistant.

Topic: {topic}

Provide:
1. Key Insights
2. Common Themes
3. Conflicts
4. Final Summary

Papers:
{content}
"""

    response = model.generate_content(prompt)

    return response.text