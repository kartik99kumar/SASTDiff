import pycparser.c_ast as ast
from structs.call import Call
from process.structref import evaluateStructRef
import copy

inputFunctions = ["scanf", "gets"]


def evaluateFuncCall(funcCall, state):

    if not isinstance(funcCall, ast.FuncCall):
        return

    funcname = funcCall.name.name
    args = funcCall.args

    call = Call(funcname)

    log = "{} called with args: ".format(funcname)

    if args is not None:

        for arg in args:

            if isinstance(arg, ast.Constant):

                value = arg.value
                call.addArg(value)
                log += "[constant \"{}\"] ".format(value)

            elif isinstance(arg, ast.ID):

                name = arg.name
                svar = state.getVariable(name)
                if funcname in inputFunctions:
                    svar.setAsInput()
                var = copy.deepcopy(svar)
                call.addArg(var)
                log += "[variable \"{}\"] ".format(name)

            elif isinstance(arg, ast.StructRef):

                field = evaluateStructRef(arg)
                if funcname in inputFunctions:
                    field.setAsInput()
                var = copy.deepcopy(field)
                call.addArg(var)
                log += "[variable \"{}\"] ".format(field.name)

            elif isinstance(arg, ast.UnaryOp):

                name = arg.expr.name
                svar = state.getVariable(name)
                if funcname in inputFunctions:
                    svar.setAsInput()
                var = copy.deepcopy(svar)
                call.addArg(var)
                log += "[variable \"{}\"] ".format(name)

            elif isinstance(arg, ast.Cast):

                if isinstance(arg.expr, ast.UnaryOp):

                    name = arg.expr.expr.name
                    svar = state.getVariable(name)
                    if funcname in inputFunctions:
                        svar.setAsInput()
                    var = copy.deepcopy(svar)
                    call.addArg(var)
                    log += "[variable \"{}\"] ".format(name)

                elif isinstance(arg.expr, ast.ID):

                    name = arg.expr.name
                    svar = state.getVariable(name)
                    if funcname in inputFunctions:
                        svar.setAsInput()
                    var = copy.deepcopy(svar)
                    call.addArg(var)
                    log += "[variable \"{}\"] ".format(name)

    return call, log
