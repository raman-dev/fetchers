from .fetcher import Fetcher

class SeleniumFetcher(Fetcher):
    def fetch(self,url) -> dict:
        print(f'selenium.fetching {url}')
        return Fetcher.get_result_dict("selenium.fetch.results", Fetcher.JSON, url)
