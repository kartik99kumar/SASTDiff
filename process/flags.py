import pycparser.c_ast as ast
from structs.variable import Variable


def evaluateFlag(arg, arglist):

    if isinstance(arg, ast.BinaryOp):

        if arg.op == "|":

            left = arg.left
            right = arg.right

            if isinstance(left, ast.BinaryOp):

                evaluateFlag(left, arglist)

            elif isinstance(left, ast.ID):

                var = Variable(left.name)
                arglist.append(var)

            if isinstance(right, ast.BinaryOp):

                evaluateFlag(right, arglist)

            elif isinstance(right, ast.ID):

                var = Variable(right.name)
                arglist.append(var)
