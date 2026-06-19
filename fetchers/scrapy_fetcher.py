from .fetcher import Fetcher

class ScrapyFetcher(Fetcher):
    def fetch(self,url) -> dict:
        print(f'scrapy.fetching {url}')

        return Fetcher.get_result_dict("scrapy.fetch.results", Fetcher.JSON, url)

