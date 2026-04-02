from collections import deque
from urllib.parse import urlparse

from services.scraper.fetcher import fetch_page
from services.scraper.utils import score_url, get_pattern, normalize_url
from services.scraper.config import MAX_PAGES, MAX_PER_PATTERN, MAX_DEPTH, DELAY_RANGE
from services.scraper.browser_manager import BrowserManager
from services.scraper.link_extractor import extract_links, is_valid_url
from services.scraper.extractor import extract_structured_chunks, clean_soup, extract_title
from services.scraper.robot_manager import RobotsManager
from collections import defaultdict
import heapq



class Crawler:

    def __init__(self, base_url, max_pages=MAX_PAGES, max_depth=MAX_DEPTH):
        self.base_url = normalize_url(base_url)
        self.max_pages = max_pages
        self.max_depth = max_depth

        self.robots = RobotsManager(self.base_url)

        self.visited = set()
        self.pattern_counts = defaultdict(int)
        self.seen_products = set()

    def is_product(self, url):
        return "/products/" in url

    def get_product_key(self, url):
        return url.split("/products/")[-1].split("?")[0]

    async def crawl(self):

        results = []
        title = ""
        queue = []

        heapq.heappush(queue, (-score_url(self.base_url), self.base_url, 0))

        browser = BrowserManager()
        await browser.start()
        
        try:
            while queue and len(self.visited) < self.max_pages:

                _, url, depth = heapq.heappop(queue)

                url = normalize_url(url)

                if url in self.visited or depth > self.max_depth:
                    continue

                if not self.robots.is_allowed(url):
                    continue

                # product deduplication
                if self.is_product(url):
                    key = self.get_product_key(url)
                    if key in self.seen_products:
                        continue
                    self.seen_products.add(key)

                pattern = get_pattern(url)

                if self.pattern_counts[pattern] >= MAX_PER_PATTERN:
                    continue

                print(f"Visiting: {url}")

                self.visited.add(url)
                self.pattern_counts[pattern] += 1

                html = await fetch_page(url, browser)
                if not html:
                    continue

                soup = clean_soup(html)

                if not title:
                    title = extract_title(soup)

                chunks = extract_structured_chunks(soup)
                results.extend(chunks)

                links = extract_links(html, self.base_url)

                for link in links:
                    link = normalize_url(link)

                    if not is_valid_url(link):
                        continue

                    if link not in self.visited:
                        heapq.heappush(
                            queue,
                            (-score_url(link), link, depth + 1)
                        )

                await self.robots.sleep()

        finally:
            await browser.close()

        return title, results