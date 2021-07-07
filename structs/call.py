from structs.variable import Variable


class Call:

    def __init__(self, name, coord):
        self.name = name
        self.args = []
        self.coord = coord

    def addArg(self, arg):
        self.args.append(arg)

    def show(self, tab=0):

        callstr = "{}function name: {} arguments: \n\n".format(
            tab*"\t", self.name)
        for arg in self.args:
            if isinstance(arg, Variable):
                callstr += arg.show(tab+1)
            elif isinstance(arg, str):
                callstr += "{}{}\n".format((tab+1)*"\t", arg)

        return callstr
