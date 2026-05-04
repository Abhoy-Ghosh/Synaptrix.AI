from dotenv import load_dotenv
from google import genai
import os
import json
import time

load_dotenv()

# -----------------------------
# CONFIG
# -----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL = "gemini-2.0-flash"

# -----------------------------
# CACHE CONFIG
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "llm_cache.json")
CACHE_TTL = 60 * 60 * 24 * 30  # 30 days


# -----------------------------
# LOAD / SAVE CACHE
# -----------------------------
def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)


# -----------------------------
# GROQ FALLBACK
# -----------------------------
def groq_llm(prompt):
    import requests

    if not GROQ_API_KEY:
        print("❌ GROQ API key missing")
        return "AI temporarily unavailable"

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=30
        )

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ Groq error:", str(e))
        return "AI response temporarily unavailable"


# -----------------------------
# SAFE CALL + CACHE + FALLBACK
# -----------------------------
def call_llm(prompt):
    cache = load_cache()
    key = prompt[:500]

    # -----------------------------
    # CACHE HIT
    # -----------------------------
    if key in cache:
        entry = cache[key]
        if time.time() - entry["timestamp"] < CACHE_TTL:
            print("⚡ LLM CACHE HIT")
            return entry["data"]

    # -----------------------------
    # TRY GEMINI
    # -----------------------------
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        result = response.text if response.text else "No output"

    except Exception as e:
        msg = str(e)

        # -----------------------------
        # FALLBACK → GROQ
        # -----------------------------
        if "429" in msg or "quota" in msg.lower():
            print("⚠️ Gemini quota exceeded → using Groq")
            result = groq_llm(prompt)

        else:
            print("❌ Gemini error:", msg)
            result = "AI temporarily unavailable"

    # -----------------------------
    # SAVE CACHE
    # -----------------------------
    cache[key] = {
        "data": result,
        "timestamp": time.time()
    }
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