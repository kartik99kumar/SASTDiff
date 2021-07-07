import pycparser.c_ast as ast
from process.decl import evaluateDecl
from process.assignment import evaluateAssignment
from process.funccall import evaluateFuncCall
from process.ret import evaluateReturn
from process.ifblock import evaluateIf
from process.assignment import evaluateAssignment
from process.whileblock import evaluateWhile
from process.dowhileblock import evaluateDoWhile
from process.forblock import evaluateFor
from structs.state import State
from utils.data import logFile


def evaluateCompound(compound, parentState):

    if not isinstance(compound, ast.Compound):
        return

    state = State()
    state.addStateVariables(parentState)

    for block in compound.block_items:

        if isinstance(block, ast.Assignment):
            evaluateAssignment(block, state)

        elif isinstance(block, ast.Decl):
            evaluateDecl(block, state)

        elif isinstance(block, ast.FuncCall):
            evaluateFuncCall(block, state)

        elif isinstance(block, ast.Return):
            evaluateReturn(block, state)

        elif isinstance(block, ast.If):
            evaluateIf(block, state)

        elif isinstance(block, ast.While):
            evaluateWhile(block, state)

        elif isinstance(block, ast.DoWhile):
            evaluateDoWhile(block, state)

        elif isinstance(block, ast.For):
            evaluateFor(block, state)

    parentState.addChild(state)
