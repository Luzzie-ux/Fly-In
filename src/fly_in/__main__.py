import sys

from fly_in import Parser, ParserError

try:
    Parser.validate(sys.argv)
    Parser.log()
except ParserError as e:
    print(str(e), file=sys.stderr)
    print("[Ending Fly-In Simulation]")
    sys.exit(1)
