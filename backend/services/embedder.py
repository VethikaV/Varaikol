from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def embed(texts: list[str]) -> list:
    return model.encode(texts).tolist()