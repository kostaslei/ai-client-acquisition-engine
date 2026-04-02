from urllib.parse import urljoin
from scraper.parser import parse_xml
from scraper.fetcher import fetch
from scraper.utils import normalize


def parse_sitemap(xml_text: str):
    root = parse_xml(xml_text)

    urls = []
    sub_sitemaps = []

    for loc in root.findall(".//{*}loc"):
        link = loc.text.strip()

        if link.endswith(".xml"):
            sub_sitemaps.append(link)
        else:
            urls.append(normalize(link))

    return urls, sub_sitemaps


def get_all_sitemap_urls(base_url: str, delay=1.0):
    sitemap_url = urljoin(base_url, "/sitemap.xml")

    to_visit = [sitemap_url]
    all_urls = set()

    while to_visit:
        sm_url = to_visit.pop()

        try:
            xml = fetch(sm_url, delay)
            urls, subs = parse_sitemap(xml)

            all_urls.update(urls)
            to_visit.extend(subs)

        except Exception:
            continue

    return list(all_urls)