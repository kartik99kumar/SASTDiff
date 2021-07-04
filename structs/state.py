from structs.variable import Variable
from structs.call import Call
import copy


class State:

    def __init__(self):
        self.variables = {}
        self.args = []
        self.log = []
        self.calls = []

    def addVariable(self, variable):

        if not isinstance(variable, Variable):
            return

        name = variable.name
        if name is not None:
            self.variables[name] = variable

    def getVariable(self, variableName):

        if variableName in self.variables:
            return self.variables[variableName]
        else:
            return None

    def addCall(self, call):

        if isinstance(call, Call):
            self.calls.append(call)

    def getCall(self, callName):

        calls = []
        if callName is None:
            return None

        for call in self.calls:
            if call.name == callName:
                calls.append(call)

        return calls

    def addArg(self, arg):

        if isinstance(arg, Variable):
            self.args.append(arg)

    def getArgs(self):
        return self.args

    def addToLog(self, log):
        self.log.append(log)

    def showLog(self, file=None):
        if file is None:
            for i, l in enumerate(self.log):
                print("{}: {}".format(i+1, l))
        else:
            log = ""
            for i, l in enumerate(self.log):
                log += "{}: {}\n".format(i+1, l)
            file.write(log)

    def snapshot(self):

        s = copy.deepcopy(self)
        return s

    def show(self, file=None):

        statestr = ""
        statestr += "args: \n\n"
        for arg in self.args:
            statestr += arg.show(1)
        statestr += "variables: \n\n"
        for var in self.variables:
            statestr += self.variables[var].show(1)
        statestr += "calls: \n\n"
        for call in self.calls:
            statestr += call.show()

        if file is None:
            return statestr
        else:
            file.write(statestr)
