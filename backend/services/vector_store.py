vector_store = []

def add_to_vector_store(chunk, embedding):
    vector_store.append({
        "chunk": chunk,
        "embedding": embedding
    })

def build_vector_store():
    from services.embedding_service import create_embedding
    from services.knowledge_service import get_knowledge_chunks

    chunks = get_knowledge_chunks()

    for chunk in chunks:
        embedding = create_embedding(chunk)

        add_to_vector_store(
            chunk,
            embedding
        )

def get_vector_store():
    return vector_store
        

if __name__ == "__main__":
    build_vector_store()

    print("Number of vectors:", len(vector_store))
