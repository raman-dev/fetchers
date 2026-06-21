"""

    purpose is what?

    launch fetcher
    launch parser

    switch fetchers if needed

"""
from fetchers import Fetcher
from parsers import Parser


class Scraper:
    def __init__(self,parser,fetcher):
        self.__check_parser_type__(parser)
        self.__check_fetcher_type__(fetcher)

        self.parser =  parser
        self.fetcher = fetcher


    def __check_parser_type__(self,parser):
        if parser is None:
            raise ValueError("fetcher cannot be None")
        if type(parser) != Parser:
            raise TypeError("fetcher is not of type fetchers.Fetcher")

    def __check_fetcher_type__(self, fetcher):
        if fetcher is None:
            raise ValueError("fetcher cannot be None")
        if type(fetcher) != Fetcher:
            raise TypeError("fetcher is not of type fetchers.Fetcher")

    def start(self,url):
        if url is None:
            raise ValueError("url cannot be None")
        fetch_result = self.fetcher.fetch(url=url)
        parse_result = self.parser.parse(fetch_result)

        return parse_result


