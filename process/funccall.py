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

    state.setLogCoord(funcCall.coord)

    funcname = funcCall.name.name
    args = funcCall.args
    coord = funcCall.coord

    call = Call(funcname, coord)

    state.addToLog("function \"{}\" called".format(call.name))

    if args is not None:

        for arg in args:

            if isinstance(arg, ast.Constant):

                value = arg.value
                call.addArg(value)
                state.addToLog("constant {} added as argument".format(value))

            elif isinstance(arg, ast.ID):

                name = arg.name
                svar = state.getVariable(name)

                if svar is None:
                    svar = Variable(name)
                    state.addVariable(svar)
                    state.addToLog(
                        "variable \"{}\" added to state".format(svar.name))

                if funcname in inputFunctions:
                    svar.setAsInput()
                    state.addToLog(
                        "variable \"{}\" set as input".format(svar.name))

                elif funcname in validationFunctions:
                    svar.setValidation()
                    state.addToLog(
                        "variable \"{}\" validation set".format(svar.name))

                var = copy.deepcopy(svar)
                call.addArg(var)
                state.addToLog(
                    "variable \"{}\" copy added as argument".format(var.name))

                if funcname not in validationFunctions:
                    svar.resetValidation()
                    state.addToLog(
                        "variable \"{}\" validation reset".format(svar.name))

            elif isinstance(arg, ast.StructRef):

                field = evaluateStructRef(arg, state)

                if funcname in inputFunctions:
                    field.setAsInput()
                    state.addToLog(
                        "variable \"{}\" set as input".format(field.name))

                elif funcname in validationFunctions:
                    field.setValidation()
                    state.addToLog(
                        "variable \"{}\" validation set".format(field.name))

                var = copy.deepcopy(field)
                call.addArg(var)
                state.addToLog(
                    "variable \"{}\" copy added as argument".format(var.name))

                if funcname not in validationFunctions:
                    field.resetValidation()
                    state.addToLog(
                        "variable \"{}\" validation reset".format(field.name))

            elif isinstance(arg, ast.UnaryOp):

                name = arg.expr.name
                svar = state.getVariable(name)

                if svar is None:
                    svar = Variable(name)
                    state.addVariable(svar)
                    state.addToLog(
                        "variable \"{}\" added to state".format(svar.name))

                if funcname in inputFunctions:
                    svar.setAsInput()
                    state.addToLog(
                        "variable \"{}\" set as input".format(svar.name))

                elif funcname in validationFunctions:
                    svar.setValidation()
                    state.addToLog(
                        "variable \"{}\" validation set".format(svar.name))

                var = copy.deepcopy(svar)
                call.addArg(var)
                state.addToLog(
                    "variable \"{}\" copy added as argument".format(var.name))

                if funcname not in validationFunctions:
                    svar.resetValidation()
                    state.addToLog(
                        "variable \"{}\" validation reset".format(svar.name))

            elif isinstance(arg, ast.Cast):

                if isinstance(arg.expr, ast.UnaryOp):

                    name = arg.expr.expr.name
                    svar = state.getVariable(name)

                    if svar is None:
                        svar = Variable(name)
                        state.addVariable(svar)
                        state.addToLog(
                            "variable \"{}\" added to state".format(svar.name))

                    if funcname in inputFunctions:
                        svar.setAsInput()
                        state.addToLog(
                            "variable \"{}\" set as input".format(svar.name))

                    elif funcname in validationFunctions:
                        svar.setValidation()
                        state.addToLog(
                            "variable \"{}\" validation set", format(svar.name))

                    var = copy.deepcopy(svar)
                    call.addArg(var)
                    state.addToLog(
                        "variable \"{}\" copy added as argument".format(var.name))

                    if funcname not in validationFunctions:
                        svar.resetValidation()
                        state.addToLog(
                            "variable \"{}\" validation reset".format(svar.name))

                elif isinstance(arg.expr, ast.ID):

                    name = arg.expr.name
                    svar = state.getVariable(name)

                    if svar is None:
                        svar = Variable(name)
                        state.addVariable(svar)
                        state.addToLog(
                            "variable \"{}\" added to state".format(svar.name))

                    if funcname in inputFunctions:
                        svar.setAsInput()
                        state.addToLog(
                            "variable \"{}\" set as input".format(svar.name))

                    elif funcname in validationFunctions:
                        svar.setValidation()
                        state.addToLog(
                            "variable \"{}\" validation set".format(svar.name))

                    var = copy.deepcopy(svar)
                    call.addArg(var)
                    state.addToLog(
                        "variable \"{}\" copy added as argument".format(var.name))

                    if funcname not in validationFunctions:
                        svar.resetValidation()
                        state.addToLog(
                            "variable \"{}\" validation reset".format(svar.name))

            elif isinstance(arg, ast.BinaryOp) and arg.op == "|":

                flaglist = []
                evaluateFlag(arg, flaglist)
                call.addArg(flaglist)
                state.addToLog("flags added as argument")

    evaluateModFunc(call, state)

    state.addCall(call)
    state.addToLog("call \"{}\" added to state".format(call.name))

    return call
