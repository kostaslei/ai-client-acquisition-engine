from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from urllib.parse import unquote

def normalize_url(url):
    url = unquote(url)

    parsed = urlparse(url)

    query = parse_qs(parsed.query)

    # remove useless params
    query.pop("variant", None)
    query.pop("utm_source", None)
    query.pop("utm_medium", None)

    clean_query = urlencode(query, doseq=True)

    normalized = parsed._replace(
        scheme="https",
        query=clean_query,
        fragment=""
    )

    return urlunparse(normalized).rstrip("/")


def get_pattern(url):
    path = urlparse(url).path.strip("/")
    parts = path.split("/")

    if len(parts) <= 1:
        return "/" + path

    parts[-1] = "*"
    return "/" + "/".join(parts)

def score_url(url):
    score = 0
    url = url.lower()

    # HIGH VALUE
    if "about" in url: score += 5
    if "contact" in url: score += 5
    if "home" in url: score += 5

    # MEDIUM
    if "service" in url: score += 4
    if "product" in url: score += 2
    if "solution" in url: score += 4
    if "course" in url: score += 3
    if "portfolio" in url: score += 3


    # LOW VALUE
    if "login" in url: score -= 5
    if "cart" in url: score -= 5
    if "privacy" in url: score -= 5
    if "calendar" in url: score -= 5
    if "cookie" in url: score -= 5
    if "legal" in url: score -= 5
    if "month" in url: score -= 5
    if "jpg" in url: score -= 5
    if "upload" in url: score -= 5
    if "blog" in url: score -= 5
    if "mail" in url: score -= 5
    if "download" in url: score -= 5
    if "page" in url: score -= 1

    return score