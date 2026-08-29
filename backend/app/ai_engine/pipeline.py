import asyncio
import time
import os
import numpy as np



from app.agents.retriever import retrieve_papers
from app.agents.summarizer import summarize
from app.agents.analyzer import analyze
from app.agents.similarity import find_similarities
from app.agents.gap_finder import find_gaps
from app.agents.insight_extractor import extract_insights
from app.agents.synthesizer import synthesize

from app.cache.cache import (
    get_cached_result,
    set_cached_result
)

from app.retrieval.vector_store import (
    add_to_index,
    search_index
)

from app.feedback.feedback_store import (
    get_feedback
)

from app.feedback.paper_feedback import (
    get_paper_score
)

from app.services.model_loader import get_embedding_model

# =========================================
# ENV
# =========================================

os.environ["HF_HUB_DOWNLOAD_TIMEOUT"] = "60"

# =========================================
# MODEL (uses shared singleton)
# =========================================


def get_model():
    return get_embedding_model()


# =========================================
# NORMALIZE TOPIC
# =========================================

def normalize_topic(topic):

    return " ".join(
        topic.strip().lower().split()
    )


# =========================================
# SAFE TEXT
# =========================================

def safe_text(x, fallback=""):

    if x is None:
        return fallback

    text = str(x).strip()

    if not text:
        return fallback

    return text


# =========================================
# DEDUPLICATION
# =========================================

def deduplicate(papers):

    seen = set()

    unique = []

    for p in papers:

        title = p.get(
            "title",
            ""
        ).strip().lower()

        if not title:
            continue

        if title in seen:
            continue

        seen.add(title)

        unique.append(p)

    return unique


# =========================================
# RELEVANCE FILTER
# =========================================

def filter_relevant(papers, topic):

    topic_words = set(
        topic.lower().split()
    )

    filtered = []

    for p in papers:

        title = p.get(
            "title",
            ""
        ).lower()

        abstract = p.get(
            "abstract",
            ""
        ).lower()

        text = title + " " + abstract

        score = 0

        for word in topic_words:

            if len(word) < 3:
                continue

            if word in text:
                score += 1

        # =================================
        # TITLE BOOST
        # =================================

        title_boost = sum(

            1 for word in topic_words

            if word in title
        )

        score += title_boost * 2

        # =================================
        # STRICT FILTER
        # =================================

        if score >= 3:

            filtered.append(p)

    return filtered


# =========================================
# KEYWORD SCORE
# =========================================

def keyword_score(text, topic):

    text = text.lower()

    topic_words = topic.lower().split()

    score = sum(

        1 for w in topic_words

        if w in text
    )

    return score / max(
        len(topic_words),
        1
    )


# =========================================
# HYBRID RANKING
# =========================================

def rerank_hybrid(

    papers,
    topic,
    query_embedding,
    embeddings

):

    scores = []

    for i, paper in enumerate(papers):

        emb = embeddings[i]

        semantic = np.dot(

            emb,
            query_embedding

        ) / (

            np.linalg.norm(emb)
            * np.linalg.norm(query_embedding)
        )

        keyword = keyword_score(

            paper.get("abstract", ""),

            topic
        )

        feedback = min(

            get_paper_score(
                paper["title"]
            ),

            1.0

        ) * 0.15

        citation = min(

            paper.get(
                "citations",
                0
            ) / 1000,

            1.0

        ) * 0.1

        final = (

            0.6 * semantic
            + 0.25 * keyword
            + feedback
            + citation
        )

        scores.append(
            (final, paper)
        )

    scores.sort(

        key=lambda x: x[0],

        reverse=True
    )

    return [

        p for _, p in scores
    ]


# =========================================
# MODE SELECTION
# =========================================

def choose_mode(

    topic,
    papers,
    user_mode=None

):

    if user_mode in [

        "fast",
        "parallel",
        "research"

    ]:

        return user_mode

    if len(papers) <= 2:

        return "fast"

    if len(topic.split()) > 5:

        return "research"

    return "parallel"


# =========================================
# PARALLEL MODE
# =========================================

async def run_parallel(

    topic,
    papers

):

    print("⚡ Parallel mode")

    loop = asyncio.get_running_loop()

    tasks = [

        loop.run_in_executor(

            None,

            summarize,

            topic,

            papers
        ),

        loop.run_in_executor(

            None,

            analyze,

            topic,

            papers
        ),

        loop.run_in_executor(

            None,

            find_gaps,

            topic,

            papers
        )
    ]

    summary, analysis, gaps = await asyncio.gather(

        *tasks,

        return_exceptions=True
    )

    summary = safe_text(summary)

    analysis = safe_text(analysis)

    gaps = safe_text(gaps)

    return (

        summary,
        analysis,
        gaps
    )


# =========================================
# RESEARCH MODE
# =========================================

async def run_sequential(

    topic,
    papers

):

    print("🧠 Sequential research mode")

    summary = safe_text(

        summarize(
            topic,
            papers
        )
    )

    analysis = safe_text(

        analyze(

            f"{topic}\n\nSummary:\n{summary}",

            papers
        )
    )

    gaps = safe_text(

        find_gaps(

            f"{topic}\n\nSummary:\n{summary}\n\nAnalysis:\n{analysis}",

            papers
        )
    )

    return (

        summary,
        analysis,
        gaps
    )


# =========================================
# MAIN PIPELINE
# =========================================

async def run_pipeline(

    topic: str,

    user_mode: str = None

):

    topic = normalize_topic(topic)

    print("🚀 PIPELINE RUNNING")

    emb_model = get_model()

    # =====================================
    # FEEDBACK
    # =====================================

    feedback = get_feedback(topic)

    bypass_cache = False

    if feedback == "bad":

        print("⚠️ Bad feedback detected")

        print("🔄 Bypassing cache")

        bypass_cache = True

    # =====================================
    # CACHE
    # =====================================

    cached = None

    if not bypass_cache:

        cached = get_cached_result(
            topic,
            user_mode
        )

    if cached:

        print("⚡ CACHE HIT")

        return cached

    # =====================================
    # QUERY EMBEDDING
    # =====================================

    query_embedding = emb_model.encode(
        [topic]
    )[0]

    # =====================================
    # VECTOR SEARCH
    # =====================================

    faiss_results = search_index(

        query_embedding,

        k=15
    )

    faiss_results = deduplicate(
        faiss_results
    )

    faiss_results = filter_relevant(

        faiss_results,

        topic
    )

    print(
        "📄 Relevant vector papers:",
        len(faiss_results)
    )

    papers = []

    # =====================================
    # FETCH FRESH PAPERS
    # =====================================

    if len(faiss_results) < 3:

        print("🌐 Fetching fresh data")

        papers = retrieve_papers(topic)

        papers = deduplicate(papers)

        if papers:

            embeddings = emb_model.encode([

                p.get("abstract", "")

                for p in papers
            ])

            add_to_index(

                embeddings,

                papers
            )

            # IMPORTANT:
            # use fresh papers directly

            faiss_results = filter_relevant(

                papers,

                topic
            )

    # =====================================
    # FALLBACK
    # =====================================

    if not faiss_results:

        print(
            "⚠️ No strongly relevant papers"
        )

        faiss_results = papers[:5]

    if not faiss_results:

        return {

            "error":
            "No relevant papers found"
        }

    # =====================================
    # EMBEDDINGS
    # =====================================

    embeddings = emb_model.encode([

        p.get("abstract", "")

        for p in faiss_results
    ])

    # =====================================
    # RANKING
    # =====================================

    top_papers = rerank_hybrid(

        faiss_results,

        topic,

        query_embedding,

        embeddings

    )[:3]

    print(
        "DEBUG: top_papers =",
        len(top_papers)
    )

    # =====================================
    # INSIGHTS
    # =====================================

    print("🧠 Extracting insights...")

    for p in top_papers:

        p["insights"] = extract_insights(

            p.get(
                "abstract",
                ""
            )
        )

        p["feedback_score"] = get_paper_score(

            p["title"]
        )

    # =====================================
    # MODE
    # =====================================

    mode = choose_mode(

        topic,

        top_papers,

        user_mode
    )

    print("⚙️ MODE:", mode)

    # =====================================
    # EXECUTION
    # =====================================

    if mode == "fast":

        print(
            "⚡ FAST MODE (single LLM call)"
        )

        from app.agents.llm_combined import (
            generate_full_report
        )

        full_report = generate_full_report(

            topic,

            top_papers
        )

        full_report = safe_text(full_report)

        summary = full_report

        analysis = full_report

        gaps = full_report

    elif mode == "parallel":

        summary, analysis, gaps = await run_parallel(

            topic,

            top_papers
        )

    else:

        summary, analysis, gaps = await run_sequential(

            topic,

            top_papers
        )

    # =====================================
    # SYNTHESIS
    # =====================================

    print("🧠 Cluster-based synthesis working...")

    synthesis = safe_text(

        synthesize(

            topic,

            top_papers
        )
    )

    # =====================================
    # SIMILARITIES
    # =====================================

    similarities = find_similarities(
        top_papers
    )

    # =====================================
    # FINAL OUTPUT
    # =====================================

    result = {

        "topic": topic,

        "top_papers": top_papers,

        "summary": safe_text(summary),

        "analysis": safe_text(analysis),

        "gaps": safe_text(gaps),

        "synthesis": synthesis,

        "similarities": similarities,

        "mode_used": mode
    }

    # =====================================
    # CACHE
    # =====================================

    result_text = str(result).strip()

    if len(result_text) > 300:

        set_cached_result(

            topic,

            mode,

            result
        )

    else:

        print(
            "⚠️ Skipping weak cache"
        )

    return result