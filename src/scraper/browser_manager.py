from playwright.async_api import async_playwright

class BrowserManager:
    def __init__(self):
        self.browser = None
        self.context = None
        self.playwright = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()

    async def fetch(self, url):
        try:
            page = await self.context.new_page()
            await page.goto(url, timeout=15000)

            # wait for content to load
            await page.wait_for_load_state("networkidle")

            content = await page.content()
            await page.close()

            return content
        except:
            return None

    async def close(self):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()