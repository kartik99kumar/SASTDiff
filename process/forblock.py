import pycparser.c_ast as ast
import process


def evaluateFor(forBlock, state):

    if not isinstance(forBlock, ast.For):
        return

    cond = forBlock.cond

    process.cond.evaluateCond(cond, state)

    stmt = forBlock.stmt

    if isinstance(stmt, ast.Compound):

        process.compound.evaluateCompound(stmt, state)
