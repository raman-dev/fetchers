from fetchers import PlaywrightFetcher
from parsers import TapologyParser

from rich import print as rprint

parser = TapologyParser()
fetcher = PlaywrightFetcher()

#should be able to pair any parser with any fetcher
test_url = "https://playwright.dev/python/docs/library"

tapology_events_url = "https://www.tapology.com/search?term=ufc&search=Submit&mainSearchFilter=events"
tapology_url = "https://www.tapology.com/fightcenter/events/141144-ufc-fight-night"
tapology_url_with_results = "https://www.tapology.com/fightcenter/events/137848-ufc-white-house"
# results = fetcher.fetch(url=test_url)
# print(results)


def playwright_fetch_test(input_url,filename=None):
    results = fetcher.fetch(url=input_url)
    #print to file for testing
    if not filename is None and len(filename.strip()) > 0:
        with open(filename.strip(), "w", encoding="utf-8") as f:
            f.write(results["results"])

def tapology_parser_test():
    rprint("PARSING MATCHUPS------------")
    with open("tapology_home.html","r",encoding="utf-8") as f:
        source = "\n".join(f.readlines())
        result = parser.parse(source,TapologyParser.ParseType.PARSE_MATCHUPS)

        rprint(result)
    #
    # rprint("PARSING RESULTS--------------")
    # with open("tapology_home_with_results.html","r",encoding="utf-8") as f:
    #     source = "\n".join(f.readlines())
    #     result = parser.parse(source,TapologyParser.ParseType.PARSE_RESULTS)
    #
    #     rprint(result)
    # rprint("PARSING EVENT--------------")
    # with open("tapology_events.html","r",encoding="utf-8") as f:
    #     source = "\n".join(f.readlines())
    #     result = parser.parse(source,TapologyParser.ParseType.PARSE_EVENT_DATA)
    #
    #     rprint(result)

# playwright_fetch_test(input_url=tapology_events_url,filename="tapology_events.html")
tapology_parser_test()
