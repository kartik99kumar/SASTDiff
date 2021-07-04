from structs.variable import Variable


class Call:

    def __init__(self, name, coord):
        self.name = name
        self.args = []
        self.coord = coord

    def addArg(self, arg):
        self.args.append(arg)

    def show(self):

        callstr = ""
        callstr += "function name: {} arguments: \n\n".format(self.name)
        for arg in self.args:
            if isinstance(arg, Variable):
                callstr += arg.show(1)
            else:
                callstr += arg

        return callstr
