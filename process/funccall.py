import pycparser.c_ast as ast
from structs.call import Call
from structs.field import Field
import copy

inputFunctions = ["scanf", "gets"]


def evaluateFuncCall(funcCall, state):

    funcname = funcCall.name.name
    args = funcCall.args

    c = Call(funcname)

    log = "{} called with args: ".format(funcname)

    if args is not None:
        for arg in args:
            if(isinstance(arg, ast.Constant)):
                value = arg.value
                c.addArg(value)
                log += "[constant \"{}\"] ".format(value)
            elif(isinstance(arg, ast.ID)):
                name = arg.name
                v = copy.deepcopy(state.variables[name])
                c.addArg(v)
                log += "[variable \"{}\"] ".format(name)
                if funcname in inputFunctions:
                    state.addAsInput(name)
            elif(isinstance(arg, ast.StructRef)):
                name = arg.name
                field = arg.field
                f = Field(field, state.variables[name])
                v = copy.deepcopy(f)
                c.addArg(v)
                log += "[variable \"{}\" field \"{}\"] ".format(name, field)
            elif(isinstance(arg, ast.Cast)):
                if(isinstance(arg.expr, ast.UnaryOp)):
                    name = arg.expr.expr.name
                    v = copy.deepcopy(state.variables[name])
                    c.addArg(v)
                    log += "[variable \"{}\"] ".format(name)
                    if funcname in inputFunctions:
                        state.addAsInput(name)
                elif(isinstance(arg.expr, ast.ID)):
                    name = arg.expr.name
                    v = copy.deepcopy(state.variables[name])
                    c.addArg(v)
                    log += "[variable \"{}\"] ".format(name)
                    if funcname in inputFunctions:
                        state.addAsInput(name)

    return c, log
