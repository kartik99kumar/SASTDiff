from tools.filepermission import evaluateBadFilePermission
from tools.buffer import evaluateBufferOverflow
from tools.bind import evaluateBind
from tools.shell import evaluateShell
from utils.table import makeTables
from utils.astBuild import makeAST
from process.funcdef import evaluateFuncDef


def evaluateCode(filename, mode):

    root = makeAST(filename, mode)
    functions, structures, globalvars = makeTables(root)

    file1 = open("logs/log.txt", "w")
    file2 = open("logs/state.txt", "w")
    file3 = open("result/result.txt", "w")

    def getCoord(w):
        return w.coord.line

    for func in functions:

        fs = evaluateFuncDef(functions[func])

        fs.showLog(file1)
        fs.show(file2)

        ws = []
        ws.extend(evaluateShell(fs))
        ws.extend(evaluateBind(fs))
        ws.extend(evaluateBufferOverflow(fs))
        ws.extend(evaluateBadFilePermission(fs))

        ws.sort(key=getCoord)

        for w in ws:
            w.show(file3)

    print("Analysis Complete. Results in result/result.txt")
