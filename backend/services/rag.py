
import chromadb
import json

from config import CHROMA_DB_PATH
from services.embedder import embed

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection("drawing_tips")

def seed_data(json_path: str = "./data/drawing_tips.json"):
    with open(json_path) as f:
        tips = json.load(f)
    docs = [t["text"] for t in tips]
    ids = [str(i) for i in range(len(docs))]
    embeddings = embed(docs)
    collection.upsert(documents=docs, embeddings=embeddings, ids=ids)

def retrieve(query: str, n=3) -> list[str]:
    query_emb = embed([query])
    results = collection.query(query_embeddings=query_emb, n_results=n)
    return results["documents"][0]