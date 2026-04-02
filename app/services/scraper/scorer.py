def cosine_similarity(a, b):
    return float(a @ b)  # fast dot product


def rank_chunks(chunks, chunk_embeddings, query_embedding):
    scored = []

    for chunk, emb in zip(chunks, chunk_embeddings):
        score = cosine_similarity(emb, query_embedding)
        scored.append((chunk, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored