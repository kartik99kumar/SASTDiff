from structs.variable import Variable
from structs.structvariable import StructVariable
import copy


class State:

    def __init__(self):
        self.variables = {}
        self.args = {}
        self.inputs = []
        self.log = []
        self.calls = []

    def addVariable(self, variable):
        self.variables[variable.name] = variable

    def addCall(self, call):
        self.calls.append(call)

    def updateVariable(self, variableName, newValue, field=None):

        if variableName in self.variables:
            if isinstance(self.variables[variableName], Variable):
                self.variables[variableName].updateValue(newValue)
            elif isinstance(self.variables[variableName], StructVariable):
                self.variables[variableName].updateFieldValue(field, newValue)

        return None

    def addDependency(self, dependeeName, dependency, dependeeField=None):
        # dependency can be field or variable or call
        if dependeeName in self.variables:
            if dependeeField is not None:
                self.variables[dependeeName].addFieldDependency(
                    dependeeField, dependency)
            else:
                self.variables[dependeeName].addDependency(dependency)

    def resetDependency(self, dependeeName, dependeeField=None):
        if dependeeName in self.variables:
            if dependeeField is not None:
                self.variables[dependeeName].resetFieldDependency(
                    dependeeField)
            else:
                self.variables[dependeeName].resetDependency()

    def getVariableValue(self, variableName, field=None):

        if variableName in self.variables:
            if isinstance(self.variables[variableName], Variable):
                return self.variables[variableName].getValue()
            elif isinstance(self.variables[variableName], StructVariable) and field is not None:
                return self.variables[variableName].getFieldValue(field)

        return None

    def addToLog(self, log):
        self.log.append(log)

    def showLog(self):
        for i, l in enumerate(self.log):
            print("{}: {}".format(i+1, l))

    def showVariables(self):
        for var in self.variables:
            self.variables[var].show()

    def addAsInput(self, name):
        self.inputs.append(name)

    def addAsArg(self, arg):
        self.args[arg.name] = arg

    def snapshot(self):

        s = copy.deepcopy(self)
        return s

    def showCalls(self):
        for call in self.calls:
            call.show()

    def showArgs(self):
        for arg in self.args:
            self.args[arg].show()

    def show(self):
        print("inputs: {}".format(self.inputs))
        print("args: ")
        self.showArgs()
        print("variables:")
        self.showVariables()
        print("calls:")
        self.showCalls()
