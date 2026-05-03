import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-mpnet-base-v2')


def find_similarities(papers):
    print("🤖 Similarity Agent working...")

    texts = [p["abstract"][:300] for p in papers]
    embeddings = model.encode(texts)

    similarities = []

    for i in range(len(papers)):
        for j in range(i + 1, len(papers)):
            score = np.dot(embeddings[i], embeddings[j]) / (
                np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
            )

            if score > 0.8:
                similarities.append({
                    "paper1": papers[i]["title"],
                    "paper2": papers[j]["title"],
                    "score": float(score)
                })

    return similarities