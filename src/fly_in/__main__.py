from sys import argv, exit
from fly_in import Parser, ParserError

try:
    Parser.validate(argv)
    for tokens in Parser.getTokens():
        print(tokens)
except ParserError:
    print("Ending Program Fly-In")
    exit(1)
