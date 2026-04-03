from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def extract_title(soup):
    # 1. <title> tag
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
        if title:
            return title

    # 2. og:title
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].strip()

    # 3. first h1
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)

    return None

def clean_soup(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "iframe"]):
        tag.decompose()

    return soup

def extract_structured_chunks(soup):
    chunks = []

    containers = soup.find_all(["section", "article"])

    if not containers:
        containers = soup.find_all(["div"], limit=20)

    for section in containers:
        block = []

        for el in section.find_all(["h1", "h2", "h3", "p", "li"]):
            text = el.get_text(strip=True)

            if len(text) > 30:
                block.append(text)

        if block:
            block = list(dict.fromkeys(block))
            chunks.append("\n".join(block))

    return chunks

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