import chromadb

from rag.embeddings import get_embedding


client = chromadb.PersistentClient(path="vectordb")

collection = client.get_collection("drawing_knowledge")


def retrieve(query, n_results=3):

    embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )

    docs = results["documents"][0]

    return "\n\n".join(docs)