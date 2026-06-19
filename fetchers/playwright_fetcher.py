from .fetcher import Fetcher

class PlaywrightFetcher(Fetcher):
    def fetch(self,url) -> dict:
        print(f'playwright.fetching {url}')
        return Fetcher.get_result_dict("playwright.fetch.results", Fetcher.JSON, url)