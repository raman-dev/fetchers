from abc import ABC, abstractmethod

class Fetcher(ABC):
    JSON = "fetcher.json"
    DICT = "fetcher.python.dict"
    @abstractmethod
    def fetch(self,url):
        pass

    @staticmethod
    def get_result_dict(self, results, format, url):
        return {"results":results,"format":format,"url":url}

class ScrapyFetcher(Fetcher):
    def fetch(self,url) -> dict:
        print(f'scrapy.fetching {url}')

        return Fetcher.get_result_dict("scrapy.fetch.results", Fetcher.JSON, url)


class SeleniumFetcher(Fetcher):
    def fetch(self,url) -> dict:
        print(f'selenium.fetching {url}')
        return Fetcher.get_result_dict("selenium.fetch.results", Fetcher.JSON, url)

class PlaywrightFetcher(Fetcher):
    def fetch(self,url) -> dict:
        print(f'playwright.fetching {url}')
        return Fetcher.get_result_dict("playwright.fetch.results", Fetcher.JSON, url)


