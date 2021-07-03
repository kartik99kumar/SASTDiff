from process.assignment import evaluateAssignment
from structs.variable import Variable
import pycparser.c_ast as ast
from structs.state import State
from process.decl import evaluateDecl
from process.assignment import evaluateAssignment
from process.funccall import evaluateFuncCall
from structs.variable import Variable


def evaluateFuncDef(funcDef):

    s = State()

    if funcDef.decl.type.args is not None:
        args = funcDef.decl.type.args.params
        for arg in args:
            var = evaluateDecl(arg, s)
            s.addAsArg(var)

    body = funcDef.body

    for b in body.block_items:

        if(isinstance(b, ast.Assignment)):
            evaluateAssignment(b, s)
        elif(isinstance(b, ast.Decl)):
            evaluateDecl(b, s)
        elif(isinstance(b, ast.FuncCall)):
            c, log = evaluateFuncCall(b, s)
            s.addCall(c)
            s.addToLog(log)

    s.show()

    return s
