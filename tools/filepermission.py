from structs.variable import Variable
from utils.warning import Warning


def evaluateBadFilePermission(state):

    warnings = []
    type = "bad file permission"

    for call in state.calls:

        name = call.name

        if name == "chmod":

            coord = call.coord

            args = call.args
            flags = args[1]

            if isinstance(flags, Variable):
                flags = []
                flags.append(args[1])

            for arg in flags:

                if isinstance(arg, Variable):

                    if arg.name == "S_IWGRP":

                        message = "file permission of {} changed to write by group".format(
                            args[0])
                        warning = Warning(coord, message, type)
                        warnings.append(warning)

                    elif arg.name == "S_IXGRP":

                        message = "file permission of {} changed to execute by group".format(
                            args[0])
                        warning = Warning(coord, message, type)
                        warnings.append(warning)

                    elif arg.name == "S_IWOTH":

                        message = "file permission of {} changed to write by others".format(
                            args[0])
                        warning = Warning(coord, message, type)
                        warnings.append(warning)

                    elif arg.name == "S_IXOTH":

                        message = "file permission of {} changed to execute by others".format(
                            args[0])
                        warning = Warning(coord, message, type)
                        warnings.append(warning)

    return warnings
