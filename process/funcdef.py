from process.assignment import evaluateAssignment
import pycparser.c_ast as ast
from structs.state import State
from process.decl import evaluateDecl
from process.assignment import evaluateAssignment
from process.funccall import evaluateFuncCall
from process.ret import evaluateReturn


def evaluateFuncDef(funcDef):

    state = State()

    if funcDef.decl.type.args is not None:

        args = funcDef.decl.type.args.params
        for arg in args:
            var = evaluateDecl(arg, state)
            state.addArg(var)

    body = funcDef.body

    for block in body.block_items:

        if isinstance(block, ast.Assignment):
            evaluateAssignment(block, state)

        elif isinstance(block, ast.Decl):
            evaluateDecl(block, state)

        elif isinstance(block, ast.FuncCall):
            call, log = evaluateFuncCall(block, state)
            state.addCall(call)
            state.addToLog(log)

        elif isinstance(block, ast.Return):
            evaluateReturn(block, state)

    return state
