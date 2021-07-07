from structs.variable import Variable
from structs.call import Call
import copy
from utils.data import logFile


class State:

    def __init__(self):

        self.variables = {}
        self.args = []
        self.log = []
        self.calls = []
        self.logCoord = None
        self.children = []

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
        self.log.append("{}: {}".format(self.logCoord, log))
        logFile.write("{}: {}\n".format(self.logCoord, log))

    def setLogCoord(self, coord):
        self.logCoord = coord

    def showLog(self, file=None):
        if file is None:
            for l in self.log:
                print(l)
        else:
            log = ""
            for l in self.log:
                log += "{}\n".format(l)
            file.write(log)

    def snapshot(self):

        s = copy.deepcopy(self)
        return s

    def show(self, tab=0, file=None):

        statestr = "{}==============================\n\n".format(tab*"\t")
        if len(self.args) > 0:
            statestr += "{}args: \n\n".format(tab*"\t")
        for arg in self.args:
            statestr += arg.show(tab+1)

        if len(self.variables) > 0:
            statestr += "{}variables: \n\n".format(tab*"\t")
        for var in self.variables:
            statestr += self.variables[var].show(tab+1)

        if len(self.calls) > 0:
            statestr += "{}calls: \n\n".format(tab*"\t")
        for call in self.calls:
            statestr += call.show(tab+1)

        statestr += "{}==============================\n\n".format(tab*"\t")

        if file is None:
            return statestr
        else:
            file.write(statestr)

    def addStateVariables(self, state):

        if not isinstance(state, State):
            return

        for varName in state.variables:
            self.addVariable(state.variables[varName])

    def addChild(self, childState):

        if isinstance(childState, State):
            self.children.append(childState)
