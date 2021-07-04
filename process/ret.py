import pycparser.c_ast as ast


def evaluateReturn(ret, state):

    if not isinstance(ret, ast.Return):
        return

    if isinstance(ret.expr, ast.ID):
        name = ret.expr.name
        var = state.getVariable(name)
        state.addToLog("function return variable \"{}\" with value \"{}\"".format(
            var.name, var.getValue()))
        return var
