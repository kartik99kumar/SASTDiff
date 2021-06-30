class Variable:

    # value is a list of variable names on which the value depends
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.deps = {}

    def updateValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def addDependency(self, dependency):
        self.deps[dependency.name] = dependency

    def resetDependency(self):
        self.deps.clear()

    def show(self):
        print("name: {} value: {} deps: {}".format(
            self.name, self.value, self.deps.keys()))
