from .fetcher import Fetcher
from playwright.sync_api import sync_playwright

class PlaywrightFetcher(Fetcher):
    def fetch(self,url) -> dict:
        print(f'playwright.fetching {url}')

        title = None
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url=url)
            title = page.title()
            browser.close()

        return Fetcher.get_result_dict({"title":title}, Fetcher.DICT, url)