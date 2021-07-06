import pycparser.c_ast as ast
import process


def evaluateCond(cond, state):

    if isinstance(cond, ast.BinaryOp):

        if isinstance(cond.left, ast.FuncCall):

            process.funccall.evaluateFuncCall(cond.left, state)

        elif isinstance(cond.left, ast.BinaryOp):

            evaluateCond(cond.left, state)

        if isinstance(cond.right, ast.FuncCall):

            process.funccall.evaluateFuncCall(cond.right, state)

        elif isinstance(cond.right, ast.BinaryOp):

            evaluateCond(cond.right, state)

    elif isinstance(cond, ast.FuncCall):

        process.funccall.evaluateFuncCall(cond, state)
