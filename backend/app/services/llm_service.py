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
# GROQ FALLBACK (SAFE)
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
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=30
        )

        if response.status_code != 200:
            print("❌ Groq API error:", response.status_code, response.text)
            return ""

        data = response.json()

        choices = data.get("choices")
        if not choices:
            print("❌ Groq malformed response:", data)
            return ""

        message = choices[0].get("message", {})
        content = message.get("content")

        if not content:
            print("❌ Groq empty content:", data)
            return ""

        return content

    except Exception as e:
        print("❌ Groq error:", str(e))
        return ""


# -----------------------------
# MAIN LLM CALL (ROBUST)
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

    result = ""

    # -----------------------------
    # TRY GEMINI
    # -----------------------------
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        result = response.text if response.text else ""

        if not result.strip():
            raise ValueError("Empty Gemini response")

    except Exception as e:
        print("⚠️ Gemini failed → switching to Groq:", str(e))

        # -----------------------------
        # ALWAYS FALLBACK
        # -----------------------------
        result = groq_llm(prompt)

    # -----------------------------
    # FINAL SAFETY
    # -----------------------------
    if not result or len(result.strip()) < 5:
        print("❌ Both Gemini & Groq failed")
        result = "AI temporarily unavailable"

    # -----------------------------
    # DEBUG LOG
    # -----------------------------
    print("LLM OUTPUT (first 120 chars):", result[:120])

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
# OPTIONAL: SUMMARIZER (COMPAT)
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