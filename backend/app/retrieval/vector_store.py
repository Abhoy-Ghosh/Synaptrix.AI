import faiss
import numpy as np

# Global index + metadata
index = None
documents = []


def create_index(embeddings, docs):
    global index, documents

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    documents = docs


def add_to_index(embeddings, docs):
    global index, documents

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

    distances, indices = index.search(query_embedding, k)

    results = []
    for i in indices[0]:
        if i < len(documents):
            results.append(documents[i])

    return results

# 1. fetch papers
# 2. embed
# 3. store in FAISS
# 4. search using FAISS

# First time:
# Fetch + embed + store

# Second time:
# Search instantly from FAISS ⚡

# fetch → embed → cosine → rank (every time)
# now: fetch → embed → store → search (FAISS)
