from urllib.parse import urljoin
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from services.scraper.config import EXCLUDED_EXTENSIONS


def is_valid_url(url):
    url = url.lower()

    # skip file types
    if any(url.endswith(ext) for ext in EXCLUDED_EXTENSIONS):
        return False

    # skip feeds / api patterns
    if any(x in url for x in ["feed", "rss", "sitemap", "api", ".atom", ".xml"]):
        return False

    return True


def is_priority(url: str) -> bool:
    keywords = [
        "about", "contact", "portfolio",
        "product", "career", "service",
        "solution", "pricing", "team"
    ]
    return any(k in url.lower() for k in keywords)


def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    base_domain = urlparse(base_url).netloc

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if href.startswith("#") or "javascript:" in href:
            continue

        full_url = urljoin(base_url, href)

        if urlparse(full_url).netloc == base_domain:
            clean_url = full_url.split("#")[0].rstrip("/")
            links.add(clean_url)

    return list(links)