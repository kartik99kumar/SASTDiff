import pycparser.c_ast as ast
import process


def evaluateDoWhile(doWhileBlock, state):

    if not isinstance(doWhileBlock, ast.DoWhile):
        return

    cond = doWhileBlock.cond

    process.cond.evaluateCond(cond, state)

    stmt = doWhileBlock.stmt

    if isinstance(stmt, ast.Compound):

        process.compound.evaluateCompound(stmt, state)
