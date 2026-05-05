import faiss
import numpy as np

# Global index + metadata
index = None
documents = []


def create_index(embeddings, docs):
    global index, documents

    if embeddings is None or len(embeddings) == 0:
        print("⚠️ No embeddings to index")
        return

    embeddings = embeddings.astype("float32")
    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]

    # 🔥 COSINE SIMILARITY INDEX
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    documents = docs


def add_to_index(embeddings, docs):
    global index, documents

    if embeddings is None or len(embeddings) == 0:
        return

    embeddings = embeddings.astype("float32")
    faiss.normalize_L2(embeddings)

    if index is None:
        create_index(embeddings, docs)
    else:
        index.add(embeddings)
        documents.extend(docs)


def search_index(query_embedding, k=5):
    global index, documents

    if index is None:
        return []

    query_embedding = np.array([query_embedding]).astype("float32")

    # 🔥 normalize query too
    faiss.normalize_L2(query_embedding)

    distances, indices = index.search(query_embedding, k)

    results = []
    for i in indices[0]:
        if 0 <= i < len(documents):
            results.append(documents[i])

    return results