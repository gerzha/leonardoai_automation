from playwright.sync_api import BrowserType, Page

from constants import HEADLESS_MODE, OPTIONS


class PagesManager:
    def __init__(self, browser_type: BrowserType):
        self._browser = None
        self._pages = []
        self._browser_type = browser_type

    def new_page(self) -> Page:
        context = self._browser.new_context()
        context.set_default_timeout(5000)
        page = context.new_page()
        self._pages.append(page)
        return page

    def new_context(self):
        return self._browser.new_context()

    def close(self):
        for page in self._pages:
            page.close()
        self._browser.close()

    def __enter__(self):
        self._browser = self._browser_type.launch(**OPTIONS)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class BasePage:
    UI_URL = ""

    def __init__(self, page: Page):
        self.page = page

    def load(self, base_url: str):
        self.page.goto(f"{base_url.rstrip('/')}/{self.UI_URL.lstrip('/')}")