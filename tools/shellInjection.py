from structs.variable import Variable
shellFunctions = ["system"]


def shellEvaluate(state):

    calls = state.calls
    for call in calls:
        if call.name in shellFunctions:
            for arg in call.args:
                if isinstance(arg, Variable):
                    if arg.name in state.inputs:
                        print("warning: shell call \"{}\" uses user input \"{}\" as argument".format(
                            call.name, arg.name))
                    else:
                        for dep in arg.deps:
                            if dep.name in state.inputs:
                                print("warning: shell call \"{}\" uses variable \"{}\" which has dependency on user input \"{}\"".format(
                                    call.name, arg.name, dep.name))
