from tools.filepermission import evaluateBadFilePermission
from tools.buffer import evaluateBufferOverflow
from tools.bind import evaluateBind
from tools.shell import evaluateShell
from utils.table import makeTables
from utils.astBuild import makeAST
from process.funcdef import evaluateFuncDef
from process.decl import evaluateDecl
from tools.securepadding import evaluatePadding
from tools.serverhostverify import evaluateHostVerify
from structs.state import State
from utils.data import logFile
from utils.data import stateFile
import datetime


def evaluateState(state):

    if not isinstance(state, State):
        return

    ws = []
    ws.extend(evaluateShell(state))
    ws.extend(evaluateBind(state))
    ws.extend(evaluateBufferOverflow(state))
    ws.extend(evaluateBadFilePermission(state))
    ws.extend(evaluatePadding(state))
    ws.extend(evaluateHostVerify(state))

    for cstate in state.children:
        ws.extend(evaluateState(cstate))

    return ws


def showState(state, tab):

    if not isinstance(state, State):
        return

    state.show(tab, stateFile)

    for cstate in state.children:
        showState(cstate, tab+1)


def getCoord(w):
    return w.coord.line


def evaluateCode(filename, mode):

    root = makeAST(filename, mode)
    functions, structures, globalvars = makeTables(root)

    resultFile = open("result/result.txt", "w")

    logFile.write("\n\nlog: {}\nfilename: {}\n\n".format(
        datetime.datetime.now(), filename))

    globalState = State()

    for var in globalvars:
        evaluateDecl(globalvars[var], globalState)

    for func in functions:
        evaluateFuncDef(functions[func], globalState)

    ws = evaluateState(globalState)
    ws.sort(key=getCoord)

    for w in ws:
        w.show(resultFile)

    showState(globalState, 0)

    print("Analysis Complete. Results in result/result.txt")

    resultFile.close()
