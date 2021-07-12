# It’s not recommended to implement custom certificate chain validation. TLS libraries provide built-in certificate validation functions that should be used.

from structs.variable import Variable
from utils.warning import Warning


def evaluateCertificates(state):

    warnings = []
    type = "certificates verification"

    for call in state.calls:

        name = call.name
        coord = call.coord

        if name == "SSL_CTX_set_verify":

            args = call.args

            if args[2].name != "NULL":

                message = "using custom verification callback {} is not recommended".format(
                    args[2].name)
                warning = Warning(coord, message, type)
                warnings.append(warning)

            elif args[1].name != "SSL_VERIFY_PEER":

                message = "use OpenSSL's built-in verification of the peer certificate using SSL_VERIFY_PEER"
                warning = Warning(coord, message, type)
                warnings.append(warning)

    return warnings
