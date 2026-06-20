from enum import Enum
from .parser import Parser
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import unicodedata
import re
from rich import print as rprint


class TapologyParser(Parser):
    DOMAIN = "https://www.tapology.com"
    class ParseType(Enum):
        PARSE_RESULTS = "parse_results"
        PARSE_MATCHUPS = "parse_matchups"

    def parse(self, source ,parseType: ParseType):
        if parseType == None:
            raise ValueError("parseType not specified")
        if type(parseType) != type(self.ParseType.PARSE_RESULTS):
            raise TypeError("parseType is not of type TapologyParser.ParseType")

        match parseType:
            case self.ParseType.PARSE_RESULTS:
                return self.parse_results(source)
            case self.ParseType.PARSE_MATCHUPS:
                return self.parse_matchups(source)

        return {"results":[]}

    def parse_results(self, source):
        return "Parsing results from Tapology"
    
    def normalizeString(self, string):
        return (
            unicodedata.normalize("NFD", string)
            .encode("ascii", "ignore")
            .decode("ascii")
            .lower()
        )
    

    def scrapeWeightlbs(self,s: str):
        # grab a 3 digit number from string
        weightPattern = re.compile("(1|2)[0-9][0-9]")
        match = weightPattern.search(s)
        if match:
            return int(match.group(0))
        return None


    def scrapePrelimStatus(self,s: str):
        isPrelimPattern = re.compile("Prelim")
        if isPrelimPattern.search(s):
            return True
        return False


    def scrapeRounds(self,s: str):
        roundsPattern = re.compile("(3|5) x 5")
        match = roundsPattern.search(s)
        if not match:
            return None
        return int(match.group(0).split()[0])

    def scrapeFighterNameAndLink(self,element, result_only=False):
        fighterPQ = pq(element)

        atag = fighterPQ('[class*="link-primary-red"]').eq(0)
        name = self.normalizeString(atag.text())

        if result_only == True:
            isWinner = False
            for span in fighterPQ("span"):
                if "Up to" in pq(span).text():
                    isWinner = True
                    break
            return {"name": name, "isWinner": isWinner}

        link = atag.attr("href")
        return {"name": name, "link": TapologyParser.DOMAIN + link}
    
    def scrapeMatchups(self,source):
        # Writing the HTML content of the parsed soup to the file
        d = pq(source)  # filename="test_0.html")
        # d -> $ in jquery
        ul = d("#sectionFightCard > ul")  # this returns pyquery object

        matchups = []
        for li in ul("li"):
            # li is of type lxml.html.HtmlElement
            matchup = {}

            # dataBoutWrapper = pq(li)("div[data-bout-wrapper]").children()[0]
            dataBoutWrapper = pq(li)("div[data-bout-wrapper]:first")
            children = pq(dataBoutWrapper).children()

            rprint(f"num children =>  {len(children)}")

            parentIndex = len(children) - 2  # second last child
            dataParent = children[parentIndex]
            fighter_a, boutInfo, fighter_b = pq(dataParent).children()

            x = self.scrapeFighterNameAndLink(fighter_a)
            y = self.scrapeFighterNameAndLink(fighter_b)
            matchup["fighters_raw"] = [x, y]
            m = pq(boutInfo).text()
            # if contains 5 x 5 -> 5 rounder
            # if contains Prelim -> on prelims else on main card
            # check for an int that is valid 115,125,135,145,155,170,185,205,265
            isRumoured = re.compile("Prelim|Main Card|Co-Main|Main Event")
            if not isRumoured.search(m):
                # not a valid matchup # print(m)
                continue
            # grab prelimStatus
            isPrelim = self.scrapePrelimStatus(m)
            # grab the weightclass
            weightlbs = self.scrapeWeightlbs(m)
            # grab rounds
            rounds = self.scrapeRounds(m)
            if not weightlbs or not rounds:  # not a valid matchup
                continue
            matchup["weight_class"] = weightlbs
            matchup["rounds"] = rounds
            matchup["isprelim"] = isPrelim
            rprint(matchup)
            matchups.append(matchup)

        return matchups
    
    def parse_matchups(self, source):
        return self.scrapeMatchups(source)
    