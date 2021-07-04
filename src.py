from utils.astBuild import makeAST
import sys
from utils.table import makeTables
from process.funcdef import evaluateFuncDef
from process.decl import evaluateDecl
from structs.state import State
from tools.shell import evaluateShell
from tools.bind import evaluateBind
from tools.buffer import evaluateBufferOverflow
from tools.filepermission import evaluateBadFilePermission

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    sys.exit("usage: python3 src.py [filename1] [filename2]...")

root = makeAST(filename)
functions, structures, globalvars = makeTables(root)

# s = State()
# print("global variables:")
# for var in globalvars:
#     evaluateDecl(globalvars[var], s)

# s.showLog()

file1 = open("logs/log.txt", "w")
file2 = open("logs/state.txt", "w")
file3 = open("result/result.txt", "w")

for func in functions:
    fs = evaluateFuncDef(functions[func])
    fs.showLog(file1)
    fs.show(file2)
    # shellEvaluate(fs)
    # ws = evaluateBind(fs)
    # ws = evaluateBufferOverflow(fs)
    # ws = evaluateBadFilePermission(fs)
    ws = evaluateShell(fs)
    for w in ws:
        w.show(file3)

print("Analysis Complete. Results in result/result.txt")
