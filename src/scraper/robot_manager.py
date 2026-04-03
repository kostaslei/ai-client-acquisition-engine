import requests
import re
import asyncio
import random
from urllib.parse import unquote
from utils.config import DELAY_RANGE

class RobotsManager:
    def __init__(self, base_url):
        self.rules = []
        self.crawl_delay = None
        self.load(base_url)

    def load(self, base_url):
        try:
            res = requests.get(base_url.rstrip("/") + "/robots.txt", timeout=5)

            for line in res.text.splitlines():
                line = line.strip()

                if line.lower().startswith("user-agent"):
                    current_user_agent = line.split(":")[1].strip()

                elif line.lower().startswith("disallow"):
                    if current_user_agent not in ["*", None]:
                        continue  # skip other bots

                    rule = line.split(":", 1)[1].strip()

                    if rule:
                        self.rules.append(self._to_regex(rule))

                elif "crawl-delay" in line.lower():
                    if current_user_agent not in ["*", None]:
                        continue

                    try:
                        self.crawl_delay = float(line.split(":")[1].strip())
                    except:
                        pass

        except:
            pass

    def _to_regex(self, rule):
        # convert robots pattern to regex
        rule = unquote(rule)
        rule = re.escape(rule)
        rule = rule.replace("\\*", ".*")

        # IMPORTANT: allow regex ranges like [a-f0-9]
        rule = rule.replace("\\[", "[").replace("\\]", "]")

        return re.compile(rule)

    def is_allowed(self, url):
        url = unquote(url)

        for rule in self.rules:
            if rule.search(url):
                print(f"NOT ALLOWED TO VISIT {url}")
                return False
        return True

    async def sleep(self):
        if self.crawl_delay:
            delay = self.crawl_delay
        else:
            delay = random.uniform(*DELAY_RANGE)

        await asyncio.sleep(delay)