# looks for bind calls that may indicate binding:
# 1. to network interfaces using INADDR_ANY
# 2. to restricted addresses

from utils.warning import Warning
from structs.call import Call
from structs.variable import Variable

allowedAddresses = ["192.168.1.2"]


def evaluateBind(state):

    warnings = []
    type = "binding to unwanted interfaces"

    for call in state.calls:

        if call.name == "bind":
            coord = call.coord
            var = call.args[1]

            if "sin_addr" in var.fields:
                innerfield = var.fields["sin_addr"]

                if "s_addr" in innerfield.fields:
                    outerfield = innerfield.fields["s_addr"]
                    deps = outerfield.getDependency()

                    if outerfield.value is not None:

                        value = outerfield.value

                        if value not in allowedAddresses:

                            message = "Binding to address {} is not allowed. Use allowed addresses for binding.".format(
                                value)
                            warning = Warning(coord, message, type)
                            warnings.append(warning)

                    elif "inet_addr" in deps:

                        inet_addr_call = deps["inet_addr"]

                        if not isinstance(inet_addr_call, Call):
                            continue

                        addr = inet_addr_call.args[0]

                        if isinstance(addr, Variable) and addr.name == "INADDR_ANY":

                            message = "Binding using INADDR_ANY is vulnerable. Use allowed addresses for binding."
                            warning = Warning(coord, message, type)
                            warnings.append(warning)

                        elif isinstance(addr, str) and addr.strip("\"") not in allowedAddresses:

                            message = "Binding to address {} is not allowed. Use allowed addresses for binding.".format(
                                addr)
                            warning = Warning(coord, message, type)
                            warnings.append(warning)

                    elif "htonl" in deps:

                        htonl_call = deps["htonl"]

                        if not isinstance(htonl_call, Call):
                            continue

                        addr = htonl_call.args[0]

                        if isinstance(addr, Variable) and addr.name == "INADDR_ANY":

                            message = "Binding using INADDR_ANY is vulnerable. Use allowed addresses for binding."
                            warning = Warning(coord, message, type)
                            warnings.append(warning)

                    elif "INADDR_ANY" in deps:

                        message = "Binding using INADDR_ANY is vulnerable. Use allowed addresses for binding."
                        warning = Warning(coord, message, type)
                        warnings.append(warning)

    return warnings
