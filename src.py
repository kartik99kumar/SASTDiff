import sys
from process.code import evaluateCode

if len(sys.argv) == 3:

    mode = sys.argv[2]
    filename = sys.argv[1]

elif len(sys.argv) == 2:

    filename = sys.argv[1]
    mode = "code"

else:

    sys.exit("usage: python3 src.py filename [mode]")

evaluateCode(filename, mode)
