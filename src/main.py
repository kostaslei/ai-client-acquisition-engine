from processing.cleaner import select_top_chunks
from embeddings.embedder import get_embedding, embed_chunks
from processing.scorer import rank_chunks
from utils.config import MAX_CHARS, QUERY
from scraper.crawler import Crawler
from llm.llm import generate_answer
import asyncio

async def main():

    base_url = ""

     # Fetch
    crawler = Crawler(base_url)
    title,chunks = await crawler.crawl()
    print(chunks)

    # Embeddings
    query_embedding = get_embedding(QUERY)
    chunk_embeddings = embed_chunks(chunks)

    # Rank
    ranked = rank_chunks(chunks, chunk_embeddings, query_embedding)
    print(ranked)

    # Select top chunks
    top_chunks = select_top_chunks(ranked, MAX_CHARS)

    # Remove duplicates    
    top_chunks = list(dict.fromkeys(top_chunks))

    # Join chunks 
    website_content = "".join(f"{value}" for value in top_chunks)

    # LLM
    response = generate_answer(title, website_content)

    print(response)

if __name__ == "__main__":
    asyncio.run(main())