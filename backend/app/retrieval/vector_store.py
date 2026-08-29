import faiss
import numpy as np

# =========================================
# GLOBAL STATE
# =========================================

index = None

documents = []

MAX_DOCS = 200


# =========================================
# RESET INDEX
# =========================================

def reset_index():

    global index, documents

    index = None

    documents = []

    print("🧹 FAISS index reset")


# =========================================
# CREATE INDEX
# =========================================

def create_index(

    embeddings,
    docs

):

    global index, documents

    if (
        embeddings is None
        or len(embeddings) == 0
    ):

        print("⚠️ No embeddings to index")

        return

    embeddings = embeddings.astype(
        "float32"
    )

    faiss.normalize_L2(
        embeddings
    )

    dim = embeddings.shape[1]

    # =====================================
    # COSINE SIMILARITY
    # =====================================

    index = faiss.IndexFlatIP(dim)

    index.add(embeddings)

    documents = docs.copy()

    print(
        f"✅ Created FAISS index "
        f"with {len(documents)} docs"
    )


# =========================================
# ADD TO INDEX
# =========================================

def add_to_index(

    embeddings,
    docs

):

    global index, documents

    if (
        embeddings is None
        or len(embeddings) == 0
    ):

        return

    embeddings = embeddings.astype(
        "float32"
    )

    faiss.normalize_L2(
        embeddings
    )

    # =====================================
    # CREATE FIRST INDEX
    # =====================================

    if index is None:

        create_index(
            embeddings,
            docs
        )

        return

    # =====================================
    # LIMIT GROWTH
    # =====================================

    if len(documents) > MAX_DOCS:

        print(
            "⚠️ FAISS limit reached"
        )

        print(
            "🧹 Resetting vector DB"
        )

        reset_index()

        create_index(
            embeddings,
            docs
        )

        return

    # =====================================
    # ADD NEW
    # =====================================

    index.add(embeddings)

    documents.extend(docs)

    print(
        f"📦 Total indexed docs: "
        f"{len(documents)}"
    )


# =========================================
# SEARCH
# =========================================

def search_index(

    query_embedding,
    k=5

):

    global index, documents

    if index is None:

        return []

    query_embedding = np.array([

        query_embedding

    ]).astype("float32")

    faiss.normalize_L2(
        query_embedding
    )

    distances, indices = index.search(

        query_embedding,

        k
    )

    results = []

    seen = set()

    for idx in indices[0]:

        if (
            0 <= idx < len(documents)
        ):

            paper = documents[idx]

            title = paper.get(
                "title",
                ""
            ).lower()

            if title in seen:
                continue

            seen.add(title)

            results.append(paper)

    return results