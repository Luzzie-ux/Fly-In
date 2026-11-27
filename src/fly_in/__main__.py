import sys

from fly_in import Analyser, AnalysisError

try:
    Analyser.validate(sys.argv)
except AnalysisError as e:
    print(str(e), file=sys.stderr)
    print("[Ending Fly-In Simulation]")
    sys.exit(1)
