from astBuild import makeAST
import sys
from table import makeTables
from process.funcdef import evaluateFuncDef
from process.decl import evaluateDecl
from structs.state import State
from tools.shellInjection import shellEvaluate
from tools.bindAddress import evaluateBind

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    sys.exit("usage: python3 src.py [filename]")

root = makeAST(filename)
functions, structures, globalvars = makeTables(root)

# s = State()
# print("global variables:")
# for var in globalvars:
#     evaluateDecl(globalvars[var], s)

# s.showLog()

file1 = open("log.txt", "w")

for func in functions:
    fs = evaluateFuncDef(functions[func])
    fs.showLog(file1)
    # fs.show()
    shellEvaluate(fs)
    evaluateBind(fs)
