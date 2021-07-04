from structs.variable import Variable
from utils.warning import Warning


def evaluateShell(state):

    warnings = []
    type = "shell injection vulnerability"

    for call in state.calls:

        name = call.name
        coord = call.coord

        if name == "system" or name == "popen":

            arg = call.args[0]

            if isinstance(arg, Variable):

                if arg.isInput == True:

                    message = "command argument \"{}\" is direct user input. Use user input validation before using it in shell commands.".format(
                        arg.name)
                    warning = Warning(coord, message, type)
                    warnings.append(warning)

                else:

                    deps = arg.getDependency()
                    for dep in deps:

                        if deps[dep].isInput == True:

                            message = "command argument \"{}\" has direct/indirect dependency on user input \"{}\"".format(
                                arg.name, dep)
                            warning = Warning(coord, message, type)
                            warnings.append(warning)

    return warnings
