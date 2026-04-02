MAX_CHARS = 5000
MAX_PAGES = 25
MAX_DEPTH = 2
MAX_PER_PATTERN = 2

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

DELAY_RANGE = (1.5, 2.5)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

EXCLUDED_EXTENSIONS = (
    ".xml", ".json", ".rss",
    ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg",
    ".zip", ".rar", ".mp4", ".mp3"
)

# semantic query
QUERY = """
company description, what the company does,
products, services, solutions, about the business,
customer value proposition
"""