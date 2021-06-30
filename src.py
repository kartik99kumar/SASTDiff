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

for func in functions:
    # print("function definition: \"{}\"".format(func))
    fs = evaluateFuncDef(functions[func])
    # fs.showLog()
    # fs.show()
    shellEvaluate(fs)
    evaluateBind(fs)
