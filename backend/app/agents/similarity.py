import numpy as np
from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    global _model
    if _model is None:
        print("🔄 Loading similarity model...")
        _model = SentenceTransformer('all-mpnet-base-v2')
    return _model


def find_similarities(papers, threshold=0.75, top_k=5):
    print("🤖 Similarity Agent working...")

    if len(papers) < 2:
        return []

    # -----------------------------
    # CLEAN TEXTS
    # -----------------------------
    valid_papers = []
    texts = []

    for p in papers:
        abstract = p.get("abstract", "").strip()
        if len(abstract) > 30:
            valid_papers.append(p)
            texts.append(abstract[:300])

    if len(valid_papers) < 2:
        return []

    model = get_model()

    # -----------------------------
    # EMBEDDINGS
    # -----------------------------
    embeddings = model.encode(texts, normalize_embeddings=True)

    # -----------------------------
    # SIMILARITY MATRIX
    # -----------------------------
    sim_matrix = np.dot(embeddings, embeddings.T)

    similarities = []

    # -----------------------------
    # EXTRACT PAIRS
    # -----------------------------
    for i in range(len(valid_papers)):
        for j in range(i + 1, len(valid_papers)):
            score = sim_matrix[i][j]

            if score >= threshold:
                similarities.append({
                    "paper1": valid_papers[i]["title"],
                    "paper2": valid_papers[j]["title"],
                    "score": round(float(score), 3)
                })

    # -----------------------------
    # SORT + LIMIT
    # -----------------------------
    similarities.sort(key=lambda x: x["score"], reverse=True)

    return similarities[:top_k]