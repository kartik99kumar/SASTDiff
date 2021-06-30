import re
pattern = '\"192[0-9\.]*\"'


def evaluateBind(state):

    for call in state.calls:
        if call.name == "bind":
            var = call.args[1]
            for field in var.fields:
                if "inet_addr" in var.fields[field].deps:
                    addr = var.fields[field].deps["inet_addr"].args[0]
                    exp = re.compile(pattern)
                    if not exp.match(addr):
                        print(
                            "warning: bind address {} is not acceptable".format(addr))
