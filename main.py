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

results = fetcher.fetch(url=tapology_url)
rprint(results)