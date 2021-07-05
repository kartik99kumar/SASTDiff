from structs.variable import Variable
import pycparser.c_ast as ast
from process.funccall import evaluateFuncCall
from process.structref import evaluateStructRef
from utils.data import validationFunctions


def evaluateAssignment(assignment, state):

    if not isinstance(assignment, ast.Assignment):
        return

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

        var.setValue(value)
        var.resetValidation()

        state.addToLog(
            "variable \"{}\" assigned value \"{}\"".format(name, value))

        if isinstance(rval, ast.ID):

            rname = rval.name
            var.resetDependency()
            rvar = state.getVariable(rname)

            if rvar is None:
                rvar = Variable(rname)
                state.addVariable(rvar)

            var.addDependency(rvar)
            state.addToLog(
                "variable \"{}\" is added as dependency of \"{}\"".format(rname, name))

        elif isinstance(rval, ast.StructRef):

            field = evaluateStructRef(rval, state)
            var.resetDependency()
            var.addDependency(field)
            state.addToLog("variable \"{}\" added as dependency of \"{}\"".format(
                field.name, name))

        elif isinstance(rval, ast.FuncCall):

            call = evaluateFuncCall(rval, state)
            var.resetDependency()
            var.addDependency(call)

            if call.name in validationFunctions:
                var.setValidation()

            state.addToLog(
                "function call \"{}\" added as dependency of variable \"{}\"".format(call.name, name))

    elif isinstance(lval, ast.StructRef):

        field = evaluateStructRef(lval, state)
        field.setValue(value)
        name = field.name

        field.resetValidation()

        state.addToLog("variable \"{}\" assigned value \"{}\"".format(
            field.name, value))

        if isinstance(rval, ast.ID):

            rname = rval.name
            field.resetDependency()
            rvar = state.getVariable(rname)

            if rvar is None:
                rvar = Variable(rname)
                state.addVariable(rvar)

            field.addDependency(rvar)
            state.addToLog(
                "variable \"{}\" is added as dependency of \"{}\"".format(rname, name))

        elif isinstance(rval, ast.StructRef):

            rfield = evaluateStructRef(rval, state)
            field.resetDependency()
            field.addDependency(rfield)
            state.addToLog("variable \"{}\" added as dependency of \"{}\"".format(
                rfield.name, name))

        elif isinstance(rval, ast.FuncCall):

            call = evaluateFuncCall(rval, state)
            field.resetDependency()
            field.addDependency(call)

            if call.name in validationFunctions:
                field.setValidation()

            state.addToLog(
                "function call \"{}\" added as dependency of variable \"{}\"".format(call.name, name))
