from sentence_transformers import SentenceTransformer
from services.scraper.config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)


def get_embedding(text: str):
    return model.encode(text, normalize_embeddings=True)


def embed_chunks(chunks: list[str]):
    return model.encode(chunks, normalize_embeddings=True)