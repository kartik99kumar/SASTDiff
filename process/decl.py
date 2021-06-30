import pycparser.c_ast as ast
from structs.variable import Variable
from structs.state import State
from structs.structvariable import StructVariable
from structs.field import Field


def evaluateDecl(decl, state):

    name = decl.name
    init = None

    if(isinstance(decl.type.type, ast.Struct)):
        structName = decl.type.type.name
        var = StructVariable(name, structName)
        state.addVariable(var)
        state.addToLog(
            "variable \"{}\" of structure \"{}\" declared".format(name, structName))
    else:
        var = Variable(name)
        state.addVariable(var)
        state.addToLog("variable \"{}\" declared".format(name))

    if(isinstance(decl.init, ast.ID)):
        init = decl.init.name
        if init in state.variables:
            value = state.variables[init].value
            var.updateValue(value)
            state.addToLog("variable \"{}\" is initialised to variable \"{}\" with value \"{}\"".format(
                name, init, value))
            state.addDependency(name, state.variables[init])
            state.addToLog(
                "variable \"{}\" added as dependency of \"{}\"".format(init, name))
    elif(isinstance(decl.init, ast.StructRef)):
        sname = decl.init.name
        field = decl.init.field
        if sname in state.variables:
            value = state.variables[sname].getFieldValue(field)
            var.updateValue(value)
            state.addToLog("variable \"{}\" is initialised to variable \"{}\" field \"{}\" with value \"{}\"".format(
                name, sname, field, value))
            f = Field(field, state.variables[sname])
            state.addDependency(name, f)
            state.addToLog("variable \"{}\" field \"{}\" added as dependency of \"{}\"".format(
                sname, field, name))
    elif(isinstance(decl.init, ast.Constant)):
        value = decl.init.value
        var.updateValue(value)
        state.addToLog(
            "variable \"{}\" is initialised to value \"{}\"".format(name, value))

    return var
