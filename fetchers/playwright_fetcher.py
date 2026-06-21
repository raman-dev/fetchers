from .fetcher import Fetcher
from playwright.sync_api import sync_playwright

class PlaywrightFetcher(Fetcher):
    DEFAULT_TIMEOUT = 60000
    def fetch(self,url) -> dict:
        print(f'playwright.fetching {url}')

        html_content = None
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url=url,timeout=self.DEFAULT_TIMEOUT)
            html_source = page.content()
            browser.close()

        return Fetcher.get_result_dict(html_source, Fetcher.DICT, url)