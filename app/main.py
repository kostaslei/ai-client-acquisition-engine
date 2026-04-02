from services.scraper.pipeline import process_website
from services.llm.llm import generate_answer
import asyncio

async def main():
    title,website_content = await process_website("https://thebreachstudios.com/")
    website_content = "".join(f"{value}" for value in website_content)

    response = generate_answer(title, website_content)

    print(response)

if __name__ == "__main__":
    asyncio.run(main())