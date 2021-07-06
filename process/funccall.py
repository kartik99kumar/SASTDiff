from os import stat
import pycparser.c_ast as ast
from structs.call import Call
from process.structref import evaluateStructRef
from structs.variable import Variable
from process.modfunc import evaluateModFunc
from process.flags import evaluateFlag
import copy
from utils.data import validationFunctions

inputFunctions = ["scanf", "gets"]


def evaluateFuncCall(funcCall, state):

    if not isinstance(funcCall, ast.FuncCall):
        return

    funcname = funcCall.name.name
    args = funcCall.args
    coord = funcCall.coord

    call = Call(funcname, coord)

    log = "{} called with args: ".format(funcname)
    alog = ""

    if args is not None:

        for arg in args:

            if isinstance(arg, ast.Constant):

                value = arg.value
                call.addArg(value)
                log += "[constant \"{}\"] ".format(value)

            elif isinstance(arg, ast.ID):

                name = arg.name
                svar = state.getVariable(name)

                if svar is None:
                    svar = Variable(name)
                    state.addVariable(svar)

                if funcname in inputFunctions:
                    svar.setAsInput()
                    alog += "\"{}\" set as Input\n".format(name)

                elif funcname in validationFunctions:
                    svar.setValidation()
                    alog += "\"{}\" validation set\n".format(name)

                var = copy.deepcopy(svar)
                call.addArg(var)

                if funcname not in validationFunctions:
                    svar.resetValidation()
                    alog += "\"{}\" validation reset\n".format(name)

                log += "[variable \"{}\"] ".format(name)

            elif isinstance(arg, ast.StructRef):

                field = evaluateStructRef(arg)

                if funcname in inputFunctions:
                    field.setAsInput()
                    alog += "\"{}\" set as Input\n".format(field.name)

                elif funcname in validationFunctions:
                    field.setValidation()
                    alog += "\"{}\" validation set\n".format(field.name)

                var = copy.deepcopy(field)
                call.addArg(var)

                if funcname not in validationFunctions:
                    field.resetValidation()
                    alog += "\"{}\" validation reset\n".format(field.name)

                log += "[variable \"{}\"] ".format(field.name)

            elif isinstance(arg, ast.UnaryOp):

                name = arg.expr.name
                svar = state.getVariable(name)

                if svar is None:
                    svar = Variable(name)
                    state.addVariable(svar)

                if funcname in inputFunctions:
                    svar.setAsInput()
                    alog += "\"{}\" set as Input\n".format(name)

                elif funcname in validationFunctions:
                    svar.setValidation()
                    alog += "\"{}\" validation set\n".format(name)

                var = copy.deepcopy(svar)
                call.addArg(var)

                if funcname not in validationFunctions:
                    svar.resetValidation()
                    alog += "\"{}\" validation reset\n".format(name)

                log += "[variable \"{}\"] ".format(name)

            elif isinstance(arg, ast.Cast):

                if isinstance(arg.expr, ast.UnaryOp):

                    name = arg.expr.expr.name
                    svar = state.getVariable(name)

                    if svar is None:
                        svar = Variable(name)
                        state.addVariable(svar)

                    if funcname in inputFunctions:
                        svar.setAsInput()
                        alog += "\"{}\" set as Input\n".format(name)

                    elif funcname in validationFunctions:
                        svar.setValidation()
                        alog += "\"{}\" validation set\n".format(name)

                    var = copy.deepcopy(svar)
                    call.addArg(var)

                    if funcname not in validationFunctions:
                        svar.resetValidation()
                        alog += "\"{}\" validation reset\n".format(name)

                    log += "[variable \"{}\"] ".format(name)

                elif isinstance(arg.expr, ast.ID):

                    name = arg.expr.name
                    svar = state.getVariable(name)

                    if svar is None:
                        svar = Variable(name)
                        state.addVariable(svar)

                    if funcname in inputFunctions:
                        svar.setAsInput()
                        alog += "\"{}\" set as Input\n".format(name)

                    elif funcname in validationFunctions:
                        svar.setValidation()
                        alog += "\"{}\" validation set\n".format(name)

                    var = copy.deepcopy(svar)
                    call.addArg(var)

                    if funcname not in validationFunctions:
                        svar.resetValidation()
                        alog += "\"{}\" validation reset\n".format(name)

                    log += "[variable \"{}\"] ".format(name)

            elif isinstance(arg, ast.BinaryOp) and arg.op == "|":

                flaglist = []
                evaluateFlag(arg, flaglist)
                call.addArg(flaglist)
                log += "[flags] "

    state.addToLog(log)
    state.addToLog(alog)
    evaluateModFunc(call, state)
    state.addCall(call)

    return call
