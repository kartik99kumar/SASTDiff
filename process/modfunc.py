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
            state.addToLog("variable \"{}\" added to state".format(dvar.name))

        if isinstance(src, Variable):

            srcName = src.name
            svar = state.getVariable(srcName)
            if svar is None:
                svar = Variable(srcName)
                state.addVariable(svar)
                state.addToLog(
                    "variable \"{}\" added to state".format(svar.name))

            dvar.resetDependency()
            state.addToLog(
                "variable \"{}\" dependency reset".format(dvar.name))

            dvar.addDependency(svar)
            state.addToLog("variable \"{}\" added as dependency of \"{}\"".format(
                svar.name, dvar.name))

    elif name == "sprintf" or name == "snprintf":

        dest = args[0]
        destName = dest.name

        dvar = state.getVariable(destName)
        if dvar is None:
            dvar = Variable(destName)
            state.addVariable(dvar)
            state.addToLog("variable \"{}\" added to state".format(dvar.name))

        dvar.resetDependency()
        state.addToLog("variable \"{}\" dependency reset".format(dvar.name))

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
                    state.addToLog(
                        "variable \"{}\" added to state".format(svar.name))

                dvar.resetDependency()
                state.addToLog(
                    "variable \"{}\" dependency reset".format(dvar.name))

                dvar.addDependency(svar)
                state.addToLog("variable \"{}\" added as dependency of \"{}\"".format(
                    svar.name, dvar.name))
