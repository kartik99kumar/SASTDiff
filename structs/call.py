from structs.variable import Variable


class Call:

    def __init__(self, name):
        self.name = name
        self.args = []

    def addArg(self, arg):
        self.args.append(arg)

    def show(self):
        print("function name: {} arguments: \n".format(self.name))
        for arg in self.args:
            if isinstance(arg, Variable):
                arg.show(1)
