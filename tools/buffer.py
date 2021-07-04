# handles scanf, fscanf, sprintf, sscanf, gets, strcat, strcpy for buffer overflow

from utils.warning import Warning


def evaluateBufferOverflow(state):

    warnings = []
    type = "buffer overflow"

    for call in state.calls:

        name = call.name
        coord = call.coord

        if name == "scanf" or name == "fscanf" or name == "sprintf" or name == "sscanf":

            args = call.args

            if name == "scanf":
                formatstring = args[0]
            elif name == "fscanf":
                formatstring = args[1]
            elif name == "sprintf":
                formatstring = args[1]

            if formatstring.find("%s") != -1:

                message = "\"{}\" is vulnerable to buffer overflow. Use \"%9s\" for example in place of \"%s\". ".format(
                    name)

                if name == "sprintf":
                    message += "\"snprintf\" is a safer alternative."

                warning = Warning(coord, message, type)
                warnings.append(warning)

        elif name == "gets":

            message = "\"gets\" is vulnerable to buffer overflow. Use \"gets_s\" in place of \"gets\""
            warning = Warning(coord, message, type)
            warnings.append(warning)

        elif name == "strcat" or name == "strcpy":

            message = "\"{}\" is vulnerable to buffer overflow. ".format(name)

            if name == "strcat":
                message += "\"strncat\" is a safer alternative."
            elif name == "strcpy":
                message += "\"strncpy\" is a safer alternative."

            warning = Warning(coord, message, type)
            warnings.append(warning)

    return warnings
