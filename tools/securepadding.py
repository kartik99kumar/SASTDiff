# OpenSSL: For RSA encryption algorithm, the recommended padding scheme is OAEP.

from structs.variable import Variable
from utils.warning import Warning


def evaluatePadding(state):

    warnings = []
    type = "insecure padding scheme"

    for call in state.calls:

        name = call.name

        if name == "RSA_public_decrypt":

            coord = call.coord

            args = call.args
            paddingScheme = args[4]

            if paddingScheme is not None and isinstance(paddingScheme, Variable):

                if paddingScheme.name != "RSA_PKCS1_OAEP_PADDING":

                    message = "padding scheme {} is not secure. RSA_PKCS1_OAEP_PADDING is recommended".format(
                        paddingScheme.name)
                    warning = Warning(coord, message, type)
                    warnings.append(warning)

    return warnings
