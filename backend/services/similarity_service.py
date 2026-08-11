import numpy as np

from services.embedding_service import create_embedding
from services.knowledge_service import get_knowledge_chunks
from services.vector_store import build_vector_store, get_vector_store


def cosine_similarity(vector_a, vector_b):
    return np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    )


def search_knowledge(query):
    query_embedding = create_embedding(query)

    vector_store = get_vector_store()

    results = []

    for item in vector_store:
        similarity = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        results.append({
            "chunk": item["chunk"],
            "similarity": similarity
        })

    results.sort(
        key=lambda result: result["similarity"],
        reverse=True
    )

    return results[0]


if __name__ == "__main__":
    result = search_knowledge("How can I add extra luggage?")

    print("----- BEST RESULT -----")
    print("Similarity:", result["similarity"])
    print("Chunk:", result["chunk"])