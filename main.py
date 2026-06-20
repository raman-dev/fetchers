from fetchers import PlaywrightFetcher
from parsers import TapologyParser

from rich import print as rprint

parser = TapologyParser()
fetcher = PlaywrightFetcher()

#should be able to pair any parser with any fetcher
test_url = "https://playwright.dev/python/docs/library"

tapology_events_url = "https://www.tapology.com/search?term=ufc&search=Submit&mainSearchFilter=events"
tapology_url = "https://www.tapology.com/fightcenter/events/141144-ufc-fight-night"
# results = fetcher.fetch(url=test_url)
# print(results)


def playwright_fetch_test(input_url):
    results = fetcher.fetch(url=input_url)
    #print to file for testing
    with open("tapology_home.html", "w", encoding="utf-8") as f:
        f.write(results["results"])

def tapology_parser_test():
    with open("tapology_home.html","r",encoding="utf-8") as f:
        source = "\n".join(f.readlines())
        result = parser.parse(source,TapologyParser.ParseType.PARSE_MATCHUPS)

        rprint(result)

tapology_parser_test()
# playwright_fetch_test(input_url=tapology_url)