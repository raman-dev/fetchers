from parser import TapologyParser

parser = TapologyParser()

result = parser.parse("hello world",TapologyParser.ParseType.PARSE_MATCHUPS)

print(result)

