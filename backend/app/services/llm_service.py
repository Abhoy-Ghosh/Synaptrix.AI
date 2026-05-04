from dotenv import load_dotenv
from google import genai
import os
import json
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.0-flash"

# FIX 2: always save next to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "llm_cache.json")
CACHE_TTL = 60 * 60 * 24 * 30 # 30 days


# -----------------------------
# LOAD / SAVE CACHE
# -----------------------------
def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)


# -----------------------------
# SAFE CALL + CACHE
# -----------------------------
def call_llm(prompt):
    cache = load_cache()
    key = prompt[:500]

    # CACHE HIT (with TTL check)
    if key in cache:
        entry = cache[key]
        if time.time() - entry["timestamp"] < CACHE_TTL:
            print("⚡ LLM CACHE HIT")
            return entry["data"]

    # CACHE MISS → CALL LLM
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        result = response.text if response.text else "No output"
    except Exception as e:
        msg = str(e)
        if "429" in msg or "quota" in msg.lower():
            return "⚠️ LLM unavailable (quota exceeded)"
        return f"LLM Error: {msg}"

    # SAVE TO CACHE
    cache[key] = {"data": result, "timestamp": time.time()}
    save_cache(cache)

    return result


# -----------------------------
# SUMMARIZE (kept for compatibility)
# -----------------------------
def summarize_papers(papers, topic):
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
    return call_llm(prompt)