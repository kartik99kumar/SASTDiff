from structs.variable import Variable
import pycparser.c_ast as ast
from process.funccall import evaluateFuncCall
from process.structref import evaluateStructRef
from utils.data import validationFunctions


def evaluateAssignment(assignment, state):

    if not isinstance(assignment, ast.Assignment):
        return

    state.setLogCoord(assignment.coord)

    rval = assignment.rvalue
    value = None

    if isinstance(rval, ast.ID):

        name = rval.name
        rvar = state.getVariable(name)
        if rvar is not None:
            value = rvar.getValue()

    elif isinstance(rval, ast.StructRef):

        field = evaluateStructRef(rval, state)
        value = field.getValue()

    elif isinstance(rval, ast.Constant):

        value = rval.value

    lval = assignment.lvalue

    if isinstance(lval, ast.ID):

        name = lval.name
        var = state.getVariable(name)

        if var is None:
            var = Variable(name)
            state.addVariable(var)
            state.addLog("variable \"{}\" added to state".format(var.name))

        var.setValue(value)
        state.addToLog("variable \"{}\" value set to {}".format(
            var.name, var.value))

        var.resetValidation()
        state.addToLog("variable \"{}\" validation reset".format(var.name))

        if isinstance(rval, ast.ID):

            rname = rval.name
            var.resetDependency()
            state.addToLog("variable \"{}\" dependency reset".format(var.name))

            rvar = state.getVariable(rname)

            if rvar is None:
                rvar = Variable(rname)
                state.addVariable(rvar)
                state.addLog(
                    "variable \"{}\" added to state".format(rvar.name))

            var.addDependency(rvar)
            state.addToLog(
                "variable \"{}\" added as dependency of \"{}\"".format(rvar.name, var.name))

        elif isinstance(rval, ast.StructRef):

            field = evaluateStructRef(rval, state)

            var.resetDependency()
            state.addToLog("variable \"{}\" dependency reset".format(var.name))

            var.addDependency(field)
            state.addToLog("variable \"{}\" added as dependency of \"{}\"".format(
                field.name, var.name))

        elif isinstance(rval, ast.FuncCall):

            call = evaluateFuncCall(rval, state)

            var.resetDependency()
            state.addToLog("variable \"{}\" dependency reset".format(var.name))

            var.addDependency(call)
            state.addToLog(
                "call \"{}\" added as dependency of \"{}\"".format(call.name, var.name))

            if call.name in validationFunctions:
                var.setValidation()
                state.addToLog(
                    "variable \"{}\" validation set".format(var.name))

    elif isinstance(lval, ast.StructRef):

        field = evaluateStructRef(lval, state)

        field.setValue(value)
        state.addToLog("variable \"{}\" value set to {}".format(
            field.name, field.value))

        name = field.name

        field.resetValidation()
        state.addToLog("variable \"{}\" validation reset".format(field.name))

        if isinstance(rval, ast.ID):

            rname = rval.name

            field.resetDependency()
            state.addToLog(
                "variable \"{}\" dependency reset".format(field.name))

            rvar = state.getVariable(rname)

            if rvar is None:
                rvar = Variable(rname)
                state.addVariable(rvar)
                state.addToLog(
                    "variable \"{}\" added to state".format(rvar.name))

            field.addDependency(rvar)
            state.addToLog(
                "variable \"{}\" is added as dependency of \"{}\"".format(rname, field.name))

        elif isinstance(rval, ast.StructRef):

            rfield = evaluateStructRef(rval, state)

            field.resetDependency()
            state.addToLog(
                "variable \"{}\" dependency reset".format(field.name))

            field.addDependency(rfield)
            state.addToLog("variable \"{}\" added as dependency of \"{}\"".format(
                rfield.name, field.name))

        elif isinstance(rval, ast.FuncCall):

            call = evaluateFuncCall(rval, state)

            field.resetDependency()
            state.addToLog(
                "variable \"{}\" dependency reset".format(field.name))

            field.addDependency(call)
            state.addToLog("call \"{}\" added as dependency of \"{}\"".format(
                call.name, field.name))

            if call.name in validationFunctions:
                field.setValidation()
                state.addToLog(
                    "variable \"{}\" validation set".format(field.name))
