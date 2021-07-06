import pycparser.c_ast as ast
import process
from structs.variable import Variable


def evaluateDecl(decl, state):

    name = decl.name
    var = Variable(name)
    state.addVariable(var)
    state.addToLog("variable \"{}\" added to state".format(var.name))

    if isinstance(decl.init, ast.ID):

        initVarName = decl.init.name
        initVar = state.getVariable(initVarName)

        if initVar is not None:

            value = initVar.getValue()
            var.setValue(value)
            state.addToLog(
                "variable \"{}\" set to value {}".format(var.name, value))

            var.addDependency(initVar)
            state.addToLog(
                "variable \"{}\" added as dependency of \"{}\"".format(initVar.name, var.name))

    elif isinstance(decl.init, ast.StructRef):

        field = process.structref.evaluateStructRef(decl.init, state)

        value = field.getValue()
        var.setValue(value)
        state.addToLog(
            "variable \"{}\" set to value {}".format(var.name, value))

        var.addDependency(field)
        state.addToLog(
            "variable \"{}\" added as dependency of \"{}\"".format(field.name, var.name))

    elif(isinstance(decl.init, ast.Constant)):

        value = decl.init.value
        var.setValue(value)
        state.addToLog(
            "variable \"{}\" set to value {}".format(var.name, value))

    return var
