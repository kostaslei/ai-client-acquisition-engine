from services.scraper.cleaner import select_top_chunks
from services.scraper.embedder import get_embedding, embed_chunks
from services.scraper.scorer import rank_chunks
from services.scraper.config import MAX_CHARS, QUERY
from services.scraper.crawler import Crawler


async def process_website(url: str):

    # Fetch
    crawler = Crawler(url)
    title,chunks = await crawler.crawl()
    print(chunks)

  
    query_embedding = get_embedding(QUERY)
    chunk_embeddings = embed_chunks(chunks)
    # Extract contacts
    #contact_info = extract_contacts(html, url)
    
    
    # Extract content on chunks
    #chunks = extract_structured_chunks(html)

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

    return (title,top_chunks)

