from process.cond import evaluateCond
import pycparser.c_ast as ast
import process


def evaluateIf(ifBlock, state):

    if not isinstance(ifBlock, ast.If):
        return

    cond = ifBlock.cond

    evaluateCond(cond, state)

    iftrue = ifBlock.iftrue

    if isinstance(iftrue, ast.Compound):

        process.compound.evaluateCompound(iftrue, state)

    iffalse = ifBlock.iffalse

    if isinstance(iffalse, ast.Compound):

        process.compound.evaluateCompound(iffalse, state)

    elif isinstance(iffalse, ast.If):

        evaluateIf(iffalse, state)
