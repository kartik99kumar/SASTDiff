# TLS/SSL libraries provide built-in hostname verification functions that should be used.

from structs.variable import Variable
from utils.warning import Warning


def evaluateHostVerify(state):

    warnings = []
    type = "server hostname not verified"
    secureSSL = []

    for call in state.calls:

        name = call.name
        coord = call.coord

        if name == "SSL_set1_host":

            args = call.args

            if args[0] is not None and isinstance(args[0], Variable):

                secureSSL.append(args[0].name)

        elif name == "SSL_connect":

            args = call.args

            if args[0] is not None and isinstance(args[0], Variable):

                if args[0].name not in secureSSL:

                    message = "server hostname for SSL/TLS connection {} not verified through SSL_set1_host".format(
                        args[0].name)
                    warning = Warning(coord, message, type)
                    warnings.append(warning)

    return warnings
