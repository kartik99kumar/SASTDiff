import pycparser.c_ast as ast
from structs.field import Field
from structs.call import Call
from process.funccall import evaluateFuncCall


def evaluateAssignment(assignment, state):

    rval = assignment.rvalue
    value = None

    if(isinstance(rval, ast.ID)):
        name = rval.name
        value = state.getVariableValue(name)
    elif(isinstance(rval, ast.FuncCall)):
        value = None
    elif(isinstance(rval, ast.StructRef)):
        name = rval.name.name
        field = rval.field.name
        value = state.getVariableValue(name, field)
    elif(isinstance(rval, ast.Constant)):
        value = rval.value

    lval = assignment.lvalue
    if(isinstance(lval, ast.ID)):
        name = lval.name
        state.updateVariable(name, value)
        state.addToLog(
            "variable \"{}\" assigned value \"{}\"".format(name, value))
        if(isinstance(rval, ast.ID)):
            rname = rval.name
            state.resetDependency(name)
            state.addDependency(name, state.variables[rname])
            state.addToLog(
                "variable \"{}\" is added as dependency of \"{}\"".format(rname, name))
        elif(isinstance(rval, ast.StructRef)):
            rname = rval.name.name
            while isinstance(rval, ast.ID):
                rname = rname.name
            rfield = rval.field.name
            f = Field(rfield, state.variables[rname])
            state.resetDependency(name)
            state.addDependency(name, f)
            state.addToLog("variable \"{}\" field \"{}\" added as dependency of \"{}\"".format(
                rname, rfield, name))
        elif(isinstance(rval, ast.FuncCall)):
            c, flog = evaluateFuncCall(rval, state)
            state.resetDependency(name)
            state.addDependency(name, c)
            state.addToLog(
                "function call added as dependency of variable \"{}\"".format(name))
            state.addToLog(flog)
    elif(isinstance(lval, ast.StructRef)):
        name = lval.name.name
        while isinstance(name, ast.ID):
            name = name.name
        field = lval.field.name
        state.updateVariable(name, value, field)
        state.addToLog("variable \"{}\" field \"{}\" assigned value \"{}\"".format(
            name, field, value))
        if(isinstance(rval, ast.ID)):
            rname = rval.name
            if rname in state.variables:
                state.resetDependency(name, field)
                state.addDependency(name, state.variables[rname], field)
                state.addToLog("variable \"{}\" added as dependency of variable \"{}\" field \"{}\"".format(
                    rname, name, field))
        elif(isinstance(rval, ast.StructRef)):
            rname = rval.name.name
            rfield = rval.field.name
            if rname in state.variables:
                f = Field(rfield, state.variables[rname])
                state.resetDependency(name, field)
                state.addDependency(name, f)
                state.addToLog("variable \"{}\" field \"{}\" added as dependency of variable \"{}\" field \"{}\"".format(
                    rname, rfield, name, field))
        elif(isinstance(rval, ast.FuncCall)):
            c, flog = evaluateFuncCall(rval, state)
            state.resetDependency(name, field)
            state.addDependency(name, c, field)
            state.addToLog(
                "function call added as dependency of variable \"{}\" field \"{}\"".format(name, field))
            state.addToLog(flog)
