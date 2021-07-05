# sscanf can be added

from structs.variable import Variable


def evaluateModFunc(funcCall, state):

    name = funcCall.name
    args = funcCall.args

    if name == "strcpy" or name == "strncpy" or name == "strcat" or name == "strncat":

        dest = args[0]
        src = args[1]

        destName = dest.name
        dvar = state.getVariable(destName)
        if dvar is None:
            dvar = Variable(destName)
            state.addVariable(dvar)

        if isinstance(src, Variable):

            srcName = src.name
            svar = state.getVariable(srcName)
            if svar is None:
                svar = Variable(srcName)
                state.addVariable(svar)

            dvar.resetDependency()
            state.addToLog("\"{}\" added as dependency of \"{}\"".format(
                svar.name, dvar.name))
            dvar.addDependency(svar)

    elif name == "sprintf" or name == "snprintf":

        dest = args[0]
        destName = dest.name
        dvar = state.getVariable(destName)
        if dvar is None:
            dvar = Variable(destName)
            state.addVariable(dvar)

        dvar.resetDependency()

        if name == "sprintf":
            srcs = args[1:]
        else:
            srcs = args[2:]

        destName = dest.name

        for src in srcs:

            if isinstance(src, Variable):

                srcName = src.name
                svar = state.getVariable(srcName)
                if svar is None:
                    svar = Variable(srcName)
                    state.addVariable(svar)

                dvar.resetDependency()
                state.addToLog("\"{}\" added as dependency of \"{}\"".format(
                    svar.name, dvar.name))
                dvar.addDependency(svar)
