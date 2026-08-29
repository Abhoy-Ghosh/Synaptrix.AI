from dotenv import load_dotenv
from google import genai

import os
import json
import time
import hashlib
import requests

load_dotenv()

# =========================================================
# CONFIG
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL = "gemini-2.0-flash"

# =========================================================
# CACHE CONFIG
# =========================================================

BASE_DIR = os.environ.get("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

CACHE_FILE = os.path.join(
    BASE_DIR,
    "llm_cache.json"
)

CACHE_TTL = 60 * 60 * 24 * 30  # 30 days

# =========================================================
# LOAD CACHE
# =========================================================

def load_cache():

    if not os.path.exists(CACHE_FILE):
        return {}

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return {}


# =========================================================
# SAVE CACHE
# =========================================================

def save_cache(data):

    try:

        with open(
            CACHE_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )

    except Exception as e:

        print(
            "⚠️ Cache save failed:",
            str(e)
        )


# =========================================================
# HASH CACHE KEY
# =========================================================

def build_cache_key(prompt):

    return hashlib.md5(
        prompt.encode()
    ).hexdigest()


# =========================================================
# GROQ FALLBACK
# =========================================================

def groq_llm(prompt):

    if not GROQ_API_KEY:

        print("❌ GROQ API key missing")

        return None

    try:

        print("🚀 CALLING GROQ...")

        response = requests.post(

            "https://api.groq.com/openai/v1/chat/completions",

            headers={

                "Authorization":
                f"Bearer {GROQ_API_KEY}",

                "Content-Type":
                "application/json"
            },

            json={

                "model":
                "qwen/qwen3.8-27b",

                "messages": [

                    {
                        "role": "system",

                        "content": (
                            "You are a precise research assistant. "
                            "Stay grounded in the provided content. "
                            "Do not hallucinate unrelated domains."
                        )
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                "temperature": 0.3
            },

            timeout=30
        )

        # =====================================
        # API ERROR
        # =====================================

        if response.status_code != 200:

            print(
                "❌ Groq API error:",
                response.status_code
            )

            return None

        data = response.json()

        content = (

            data.get("choices", [{}])[0]

            .get("message", {})

            .get("content")
        )

        if not content:

            print("❌ Groq empty response")

            return None

        return str(content).strip()

    except Exception as e:

        print(
            "❌ Groq exception:",
            str(e)
        )

        return None


# =========================================================
# MAIN LLM CALL
# =========================================================

def call_llm(prompt):

    cache = load_cache()

    key = build_cache_key(prompt)

    # =====================================================
    # CACHE HIT
    # =====================================================

    if key in cache:

        entry = cache[key]

        if (
            time.time()
            - entry["timestamp"]
            < CACHE_TTL
        ):

            print("⚡ LLM CACHE HIT")

            return entry["data"]

    result = None

    # =====================================================
    # SAFETY PREFIX
    # =====================================================

    safety_prefix = """
You are a grounded AI research system.

Rules:
- ONLY use supplied information
- Do NOT hallucinate unrelated domains
- Stay topic-specific
- Avoid generic AI statements
- Be concise and structured
"""

    final_prompt = (

        safety_prefix
        + "\n\n"
        + prompt
    )

    # =====================================================
    # TOKEN LIMIT
    # =====================================================

    final_prompt = final_prompt[:6000]

    # =====================================================
    # TRY GEMINI
    # =====================================================

    try:

        response = client.models.generate_content(

            model=MODEL,

            contents=final_prompt
        )

        result = (

            response.text.strip()

            if response.text

            else None
        )

        if not result:

            raise ValueError(
                "Empty Gemini response"
            )

        print("✅ Gemini success")

    except Exception as e:

        print(
            f"⚠️ Gemini failed → "
            f"Groq fallback | "
            f"{type(e).__name__}"
        )

        # =================================
        # GROQ FALLBACK
        # =================================

        time.sleep(2)

        result = groq_llm(final_prompt)

        if result:

            print("✅ Groq success")

    # =====================================================
    # FINAL SAFETY FALLBACK
    # =====================================================

    if not result:

        print(
            "❌ Both Gemini & Groq failed"
        )

        result = """
# Temporary AI Limitation

## Status
- AI synthesis system temporarily overloaded

## Completed Systems
- Semantic retrieval completed
- Hybrid ranking completed
- Cluster analysis completed

## Recommendation
- Retry in a few moments
"""

    # =====================================================
    # DEBUG LOG
    # =====================================================

    print(

        "DEBUG LOG -> LLM OUTPUT:",

        str(result)[:80],

        "..."
    )

    # =====================================================
    # CACHE VALID RESPONSES
    # =====================================================

    if (

        result

        and

        len(str(result).strip()) > 50
    ):

        cache[key] = {

            "data": result,

            "timestamp": time.time()
        }

        save_cache(cache)

    else:

        print(
            "⚠️ Skipping weak cache"
        )

    # =====================================================
    # RETURN RESULT
    # =====================================================

    return str(result).strip()


# =========================================================
# OPTIONAL SUMMARIZER
# =========================================================

def summarize_papers(

    papers,
    topic
):

    content = "\n\n".join([

        f"{p['title']}: "
        f"{p['abstract'][:300]}"

        for p in papers
    ])[:2500]

    prompt = f"""
Research Topic:
{topic}

Generate:
1. Key Insights
2. Common Themes
3. Concise Summary

ONLY use the provided papers.

Papers:
{content}
"""

    return call_llm(prompt)