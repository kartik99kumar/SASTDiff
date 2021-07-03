import pycparser.c_ast as ast
from structs.variable import Variable
from process.structref import evaluateStructRef


def evaluateDecl(decl, state):

    name = decl.name
    var = Variable(name)
    state.addVariable(var)

    if isinstance(decl.type.type, ast.Struct):

        structName = decl.type.type.name
        state.addToLog(
            "variable \"{}\" of structure \"{}\" declared".format(name, structName))

    else:

        state.addToLog("variable \"{}\" declared".format(name))

    init = None

    if isinstance(decl.init, ast.ID):

        initVarName = decl.init.name
        initVar = state.getVariable(initVarName)

        if initVar is not None:

            value = initVar.getValue()
            var.setValue(value)
            state.addToLog("variable \"{}\" is initialised to variable \"{}\" with value \"{}\"".format(
                name, initVarName, value))

            var.addDependency(initVar)
            state.addToLog(
                "variable \"{}\" added as dependency of \"{}\"".format(initVarName, name))

    elif isinstance(decl.init, ast.StructRef):

        field = evaluateStructRef(decl.init, state)
        value = field.getValue()
        var.setValue(value)
        state.addToLog("variable \"{}\" is initialised to field \"{}\" with value {}".format(
            name, field.name, value))
        var.addDependency(field)
        state.addToLog(
            "variable \"{}\" added as dependency of \"{}\"".format(field.name, name))

    elif(isinstance(decl.init, ast.Constant)):

        value = decl.init.value
        var.setValue(value)
        state.addToLog(
            "variable \"{}\" is initialised to value \"{}\"".format(name, value))

    return var
