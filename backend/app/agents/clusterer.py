import numpy as np
from app.services.model_loader import get_embedding_model


def cluster_papers(papers, threshold=0.75):
    print("🧠 Clustering papers...")

    if len(papers) < 2:
        return [papers]

    model = get_embedding_model()
    texts = [p["abstract"][:300] for p in papers]
    embeddings = model.encode(texts, normalize_embeddings=True)

    sim_matrix = np.dot(embeddings, embeddings.T)

    clusters = []
    visited = set()

    for i in range(len(papers)):
        if i in visited:
            continue

        cluster = [papers[i]]
        visited.add(i)

        for j in range(len(papers)):
            if j in visited:
                continue

            if sim_matrix[i][j] >= threshold:
                cluster.append(papers[j])
                visited.add(j)

        clusters.append(cluster)

    return clusters