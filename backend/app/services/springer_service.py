import os
import re
import time
import requests

from dotenv import load_dotenv

load_dotenv()

# =========================================
# API CONFIG
# =========================================

SPRINGER_META_API_KEY = os.getenv(
    "SPRINGER_META_API_KEY"
)

BASE_URL = (
    "https://api.springernature.com/meta/v2/json"
)

HEADERS = {

    "User-Agent":
    "SynaptrixAI/1.0"
}


# =========================================
# QUERY OPTIMIZATION
# =========================================

def optimize_query(query):

    q = query.lower()

    replacements = {

        "large language model":
        "\"large language model\" OR LLM",

        "large language models":
        "\"large language models\" OR LLMs",

        "llm":
        "\"large language model\"",

        "rag":
        "\"retrieval augmented generation\"",

        "ai agents":
        "\"AI agents\" OR \"autonomous agents\"",

        "multimodal":
        "\"multimodal AI\"",

        "gpt":
        "\"GPT\" OR transformer",

        "transformer":
        "\"transformer model\""
    }

    for k, v in replacements.items():

        q = q.replace(k, v)

    return q


# =========================================
# CLEAN HTML
# =========================================

def clean_html(text):

    if not text:
        return ""

    text = re.sub(

        r"<.*?>",

        "",

        text
    )

    text = re.sub(

        r"\s+",

        " ",

        text
    )

    return text.strip()


# =========================================
# LOCAL RELEVANCE FILTER
# =========================================

def is_relevant(

    title,
    abstract,
    query

):

    text = (

        title + " " + abstract

    ).lower()

    words = query.lower().split()

    score = 0

    # =====================================
    # BASIC TERM MATCHING
    # =====================================

    for word in words:

        if len(word) < 3:
            continue

        if word in text:
            score += 1

    # =====================================
    # TITLE BOOST
    # =====================================

    title_lower = title.lower()

    title_score = sum(

        1 for word in words

        if word in title_lower
    )

    score += title_score * 2

    # =====================================
    # AI DOMAIN BOOST
    # =====================================

    ai_terms = [

        "llm",
        "language model",
        "transformer",
        "gpt",
        "bert",
        "generative ai",
        "multimodal",
        "retrieval augmented generation",
        "rag",
        "agentic",
        "foundation model"
    ]

    if any(

        term in text

        for term in ai_terms
    ):

        score += 5

    # =====================================
    # STRICT FILTER
    # =====================================

    return score >= 4


# =========================================
# FETCH SPRINGER PAPERS
# =========================================

def fetch_springer_papers(

    query,
    max_results=5,
    retry=3

):

    print("📗 Fetching from Springer...")

    if not SPRINGER_META_API_KEY:

        print("❌ Missing Springer API key")

        return []

    # =====================================
    # QUERY OPTIMIZATION
    # =====================================

    optimized_query = optimize_query(
        query
    )

    # =====================================
    # BETTER SEARCH
    # =====================================

    params = {

        "q": (
            f'title:({optimized_query}) '
            f'OR abstract:({optimized_query})'
        ),

        "p": max_results,

        "s": "relevance",

        "api_key":
        SPRINGER_META_API_KEY
    }

    for attempt in range(retry):

        try:

            response = requests.get(

                BASE_URL,

                params=params,

                headers=HEADERS,

                timeout=30
            )

            # =================================
            # RATE LIMIT
            # =================================

            if response.status_code == 429:

                print(

                    f"⏳ Springer rate limited "

                    f"(Attempt {attempt+1}/{retry})"
                )

                time.sleep(2)

                continue

            # =================================
            # API ERROR
            # =================================

            if response.status_code != 200:

                print(

                    "❌ Springer API error:",

                    response.status_code
                )

                return []

            data = response.json()

            records = data.get(

                "records",

                []
            )

            papers = []

            # =================================
            # PARSE RECORDS
            # =================================

            for record in records:

                title = record.get(

                    "title",

                    ""
                ).strip()

                abstract = record.get(

                    "abstract",

                    ""
                )

                abstract = clean_html(
                    abstract
                )

                # =============================
                # SKIP WEAK RECORDS
                # =============================

                if not title or not abstract:
                    continue

                # =============================
                # CONTENT TYPE FILTER
                # =============================

                content_type = record.get(

                    "contentType",

                    ""
                ).lower()

                if "article" not in content_type:

                    continue

                # =============================
                # LOCAL RELEVANCE FILTER
                # =============================

                if not is_relevant(

                    title,
                    abstract,
                    query
                ):

                    continue

                # =============================
                # BUILD PAPER
                # =============================

                papers.append({

                    "title": title,

                    "abstract": abstract,

                    "year": record.get(

                        "publicationDate",

                        "2020"
                    )[:4],

                    "citations": 0,

                    "source": "springer"
                })

            print(

                f"✅ Springer returned "

                f"{len(papers)} relevant papers"
            )

            return papers

        except requests.Timeout:

            print(

                f"⏳ Springer timeout "

                f"(Attempt {attempt+1}/{retry})"
            )

            time.sleep(2)

        except requests.RequestException as e:

            print(

                "❌ Springer request error:",

                str(e)
            )

            time.sleep(2)

        except Exception as e:

            print(

                "❌ Springer unexpected error:",

                str(e)
            )

            return []

    print("❌ Springer failed after retries")

    return []