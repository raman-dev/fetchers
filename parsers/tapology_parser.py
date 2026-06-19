from enum import Enum
from .parser import Parser


class TapologyParser(Parser):
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

    def parse_matchups(self, source):
        return "Parsing matchups from Tapology"