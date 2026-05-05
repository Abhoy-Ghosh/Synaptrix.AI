import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-mpnet-base-v2')


def find_similarities(papers, threshold=0.75, top_k=5):
    print("🤖 Similarity Agent working...")

    if len(papers) < 2:
        return []

    texts = [p.get("abstract", "")[:300] for p in papers]

    # -----------------------------
    # EMBEDDINGS
    # -----------------------------
    embeddings = model.encode(texts, normalize_embeddings=True)

    # -----------------------------
    # COSINE SIM MATRIX (FAST)
    # -----------------------------
    sim_matrix = np.dot(embeddings, embeddings.T)

    similarities = []

    # -----------------------------
    # EXTRACT PAIRS
    # -----------------------------
    for i in range(len(papers)):
        for j in range(i + 1, len(papers)):
            score = sim_matrix[i][j]

            if score >= threshold:
                similarities.append({
                    "paper1": papers[i]["title"],
                    "paper2": papers[j]["title"],
                    "score": round(float(score), 3)
                })

    # -----------------------------
    # SORT + LIMIT
    # -----------------------------
    similarities = sorted(similarities, key=lambda x: x["score"], reverse=True)

    return similarities[:top_k]