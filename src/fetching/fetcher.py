import requests
from utils.config import HEADERS


def fetch_requests(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=5)
        if len(res.text) < 1000:
            return None
        return res.text
    except:
        return None


async def fetch_page(url, browser_manager):
    html = fetch_requests(url)
    if html:
        return html

    return await browser_manager.fetch(url)