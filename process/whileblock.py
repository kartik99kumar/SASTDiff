import pycparser.c_ast as ast
import process


def evaluateWhile(whileBlock, state):

    if not isinstance(whileBlock, ast.While):
        return

    cond = whileBlock.cond

    process.cond.evaluateCond(cond, state)

    stmt = whileBlock.stmt

    if isinstance(stmt, ast.Compound):

        process.compound.evaluateCompound(stmt, state)
