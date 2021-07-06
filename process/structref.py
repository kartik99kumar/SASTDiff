import pycparser.c_ast as ast
from structs.variable import Variable


def evaluateStructRef(ref, state):

    if not isinstance(ref, ast.StructRef):
        return

    field = ref.field.name
    name = ref.name

    if isinstance(name, ast.StructRef):

        parent = evaluateStructRef(name, state)
        f = parent.getField(field)

        if f is not None:
            return f

        else:

            parent.addField(field)
            f = parent.getField(field)
            state.addToLog("\"{}\" added as field of \"{}\"".format(
                f.name, parent.name))

            return f

    elif isinstance(name, ast.ID):

        parent = state.getVariable(name.name)

        if parent is not None:

            f = parent.getField(field)

            if f is not None:
                return f

            else:

                parent.addField(field)
                f = parent.getField(field)
                state.addToLog("\"{}\" added as field of \"{}\"".format(
                    f.name, parent.name))

                return f

        else:

            parent = Variable(name.name)
            state.addVariable(parent)
            state.addToLog(
                "variable \"{}\" added to state".format(parent.name))

            parent.addField(field)
            f = parent.getField(field)
            state.addToLog("\"{}\" added as field of \"{}\"".format(
                f.name, parent.name))

            return f
