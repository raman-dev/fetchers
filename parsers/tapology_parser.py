from datetime import datetime
from enum import Enum
from .parser import Parser
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import unicodedata
import re
from rich import print as rprint


class TapologyParser(Parser):
    DOMAIN = "https://www.tapology.com"

    class ParseType(Enum):
        PARSE_RESULTS = "parse_results"
        PARSE_MATCHUPS = "parse_matchups"
        PARSE_EVENT_DATA = "parse_event_data"
        PARSE_FIGHTER_DATA = "parse_fighter_data"

    def parse(self, source, parseType: ParseType):
        if parseType is None:
            raise ValueError("parseType not specified")
        if type(parseType) != type(self.ParseType.PARSE_RESULTS):
            raise TypeError("parseType is not of type TapologyParser.ParseType")

        match parseType:
            case TapologyParser.ParseType.PARSE_RESULTS:
                return self.parse_results(source)
            case TapologyParser.ParseType.PARSE_MATCHUPS:
                return self.parse_matchups(source)
            case TapologyParser.ParseType.PARSE_EVENT_DATA:
                return self.parse_event_link(source)

        return {"results": []}

    def parse_event_link(self, source):
        return self.scrapeEventLink(source)

    def scrapeEventLink(self, source: str):
        soup = BeautifulSoup(source, "html.parser")
        table = soup.find("table", class_="fcLeaderboard")
        # print(table.tbody)
        today = datetime.now().date()
        rows = table.findAll("tr")
        result = {"link": "", "date": None}
        for i, row in enumerate(rows):
            if i == 0:
                continue
            data = row.findAll("td")
            # get href value from data object
            data_event_title = data[0].a.text.strip()
            # skip non fight nights and non ppvs
            if re.search(r"(UFC\s+([0-9]+))|UFC\s+Fight\s+Night", data_event_title) is None:
                # print(data_event_title,'not a ufc event')
                continue
            data_link = data[0].a["href"]
            # get date from data object
            data_date = datetime.strptime(data[2].text.strip(), "%Y.%m.%d").date()
            # compare today and date when the distance from today and date increases break loop
            # print(data_event_title,data_date)
            if data_date < today:
                break
            result["link"] = self.DOMAIN + data_link
            result["date"] = str(data_date)
        # print(result)
        return result

    def scrapeResults(self, source):
        # d = pq(filename="results_test.html",encoding='utf-8')
        d = pq(source)
        ul = d("#sectionFightCard > ul")  # this returns pyquery object
        matchupResults = []
        for i, li in enumerate(ul("li")):
            # li is of type lxml.html.HtmlElement
            # dataBoutWrapper = pq(li)("div[data-bout-wrapper]").children()[0]
            dataBoutWrapper = pq(li)("div[data-bout-wrapper]:first")

            children = pq(dataBoutWrapper).children()
            # rprint(f"num children => {len(children)}")
            methodDataParent = children[0]
            resultDataParent = children[1]

            methods = []
            for span in pq(methodDataParent)("span"):
                methods.append(pq(span).text())
            # rprint(f"methods => {methods}")
            if len(methods) == 0:
                continue
            _, method, roundTimes = methods

            fighter_a, _, fighter_b = pq(resultDataParent).children()

            x = self.scrapeFighterNameAndLink(fighter_a, result_only=True)
            y = self.scrapeFighterNameAndLink(fighter_b, result_only=True)

            result = {"fighters": [x, y]}

            # non decision fromat is M:SS Round x of y
            # decision is full time
            method = method.split(",")[0].lower()
            if "decision" in method:
                result["method"] = "decision"
            elif "ko/tko" in method:
                result["method"] = "ko"
            elif "submission" in method:
                result["method"] = "submission"
            elif "draw" in method:
                result["method"] = "draw"
            else:
                result["method"] = "no contest"

            # print(roundTimes,result['method'],method)
            if result["method"] == "decision" or result["method"] == "draw":
                # rounds = 3 or 5
                # time  = 15:00 or 25:00
                if "15:00" in roundTimes:
                    result["final_round"] = "3"
                else:
                    result["final_round"] = "5"  # last round of fight
                result["time"] = "5:00"  # final round time
            else:
                # format is Round X of Y
                # M:SS Round X of Y
                timeMatch = re.search(r"[0-5]\:[0-5][0-9]", roundTimes)
                roundMatch = re.search(r"Round [1-5] of [1-5]", roundTimes)
                result["time"] = timeMatch.group(0)
                result["final_round"] = re.search(r"[1-5]", roundMatch.group(0)).group(0)
            # print(result)
            matchupResults.append(result)
        return matchupResults

    def parse_results(self, source):
        return self.scrapeResults(source)

    def normalizeString(self, string):
        return (
            unicodedata.normalize("NFD", string)
            .encode("ascii", "ignore")
            .decode("ascii")
            .lower()
        )

    def scrapeWeightlbs(self, s: str):
        # grab a 3 digit number from string
        weightPattern = re.compile("(1|2)[0-9][0-9]")
        match = weightPattern.search(s)
        if match:
            return int(match.group(0))
        return None

    def scrapePrelimStatus(self, s: str):
        isPrelimPattern = re.compile("Prelim")
        if isPrelimPattern.search(s):
            return True
        return False

    def scrapeRounds(self, s: str):
        roundsPattern = re.compile("(3|5) x 5")
        match = roundsPattern.search(s)
        if not match:
            return None
        return int(match.group(0).split()[0])

    def scrapeFighterNameAndLink(self, element, result_only=False):
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

    def scrapeMatchups(self, source):
        # Writing the HTML content of the parsed soup to the file
        d = pq(source)  # filename="test_0.html")
        title = d("h2").text()
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

        return {'title':title,'matchups':matchups}

    def scrapeFighter(self, source: str):
        soup = BeautifulSoup(source, "html.parser")

        fighterNameRecord = soup.find_all("div", class_="leading-tight")
        nameElement, recordElement = fighterNameRecord
        full_name = self.normalizeString(nameElement.text.strip())

        record = recordElement.text.strip().split("-")
        # print(record)
        wins = int(record[0])
        losses = int(record[1])
        draws = int(record[2])

        names = list(map(lambda x: x.lower(), full_name.split(" ")))
        name_index = "-".join(names)
        print("parsing => ", full_name, name_index)

        first_name = names[0]
        last_name = " ".join(names[1:])  # full_name.split(' ')[-1]

        fighterData = {}
        fighterData["first_name"] = first_name
        fighterData["last_name"] = last_name
        fighterData["wins"] = wins
        fighterData["losses"] = losses
        fighterData["draws"] = draws
        fighterData["name_index"] = name_index

        fighterDetails = soup.find("div", id="standardDetails")
        self.scrapeFighterDetails(str(fighterDetails), fighterData)
        return fighterData

    def scrapeFighterDetails(self, fighterDetailsDiv, fighterData) -> dict:
        data = []
        result = pq(fighterDetailsDiv)("span")
        n = len(result)
        for i in range(0, n - 1):
            data.append(pq(result[i]).text())
        """
        0 'Gabriel Miranda' : name 
        1 'Fly' : nickname
        2 '17-6-0 (Win-Loss-Draw)' : record
        3 '1 Win': streak
        4 '34'   : age
        5 '1990 Mar 25': date-of-birth
        6 '5\'11" (180cm)' : height
        7 '71.0" (180cm)': reach
        8 'Featherweight' : weightclass
        9 '145.0 lbs': last weigh-in
            'Astra Fight Team'
            'September 09, 2023 in UFC'
            '$0 USD'
            'Telêmaco Borba, Paraná, Brazil' 

            2025-08-10 new query result structure
            0 name
            1 nickname
            2 record
            3 streak
            4 


            """
        height_pattern = re.compile(r"(\d)'(\d{1,2})\"\s+\(\d{3}cm\)")
        dob_pattern = re.compile(r"(\d{4})\s+(\w{3})\s+(\d{1,2})")
        reach_pattern = re.compile(r"((\d{2}\.\d+)|(\d{2}))\"\s+\(\d{3}cm\)")

        print(data)
        weightClassSet = set(
            [
                "n/a",
                "atomweight",
                "strawweight",
                "flyweight",
                "bantamweight",
                "featherweight",
                "lightweight",
                "welterweight",
                "middleweight",
                "light_heavyweight",
                "heavyweight",
                "catch_weight",
            ]
        )
        # height_string = data[6]
        # 3 height values if both feet'inch" and cm are present
        # 1 height value if only cm is present
        fighterData["height"] = 0
        fighterData["reach"] = 0
        fighterData["date_of_birth"] = "N/A"
        fighterData["weight_class"] = "lightweight"
        for d in data:
            weight_class = d.replace(" ", "_").lower()
            height_match = re.search(height_pattern, d)  # try feet'inch"
            reach_match = re.search(reach_pattern, d)
            dob_match = re.search(dob_pattern, d)
            # height_inches = 0
            # if len(height_match) == 1:
            #     height_inches = math.floor(int(height_match[0]) / 2.54)
            # if len(height_match) > 1:
            #     height_inches = int(height_match[0])*12 + int(height_match[1])
            if height_match:
                feet, inches = map(int, height_match.groups())
                height_inches = feet * 12 + inches
                fighterData["height"] = height_inches
            elif reach_match:
                reach_val = float(reach_match.group(1))
                reach_inches = int(round(reach_val))
                fighterData["reach"] = reach_inches
            elif weight_class != "n/a" and weight_class in weightClassSet:
                fighterData["weight_class"] = (
                    weight_class.upper()
                )  # first lower to query then upper to reference wtf
            elif dob_match:
                print("dob_string", d)
                dob = datetime.strptime(d, "%Y %b %d").date()
                fighterData["date_of_birth"] = dob

    def parse_matchups(self, source):
        return self.scrapeMatchups(source)
