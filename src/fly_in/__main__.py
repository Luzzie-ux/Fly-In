from sys import argv, exit, stderr
from fly_in import Parser, ParserError

try:
    Parser.validate(argv)
except ParserError as e:
    print(str(e), file=stderr)
    print("[Ending Fly-In Simulation]")
    exit(1)
