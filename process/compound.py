import pycparser.c_ast as ast
from process.decl import evaluateDecl
from process.assignment import evaluateAssignment
from process.funccall import evaluateFuncCall
from process.ret import evaluateReturn
from process.ifblock import evaluateIf
from process.assignment import evaluateAssignment


def evaluateCompound(compound, state):

    if not isinstance(compound, ast.Compound):
        return

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
