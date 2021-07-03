from pycparser.c_ast import PtrDecl


class Variable:

    def __init__(self, name):
        self.name = name
        self.value = None
        self.fields = {}
        self.deps = {}
        self.isInput = False

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def addField(self, fieldName):

        field = Variable(fieldName)
        self.fields[fieldName] = field

    def getField(self, fieldName):

        if fieldName in self.fields:
            return self.fields[fieldName]
        else:
            return None

    def getDependency(self):
        deps = {}
        for dep in self.deps:
            deps[dep] = self.deps[dep]
            if isinstance(deps[dep], Variable):
                rdeps = self.deps[dep].getDependency()
                deps.update(rdeps)
        return deps

    def addDependency(self, dep):
        name = dep.name
        if name is not None:
            self.deps[name] = dep

    def resetDependency(self):
        self.deps.clear()

    def setAsInput(self):
        self.isInput = True

    def show(self, tab=0):
        print("{}variable name: {} value: {}".format(
            tab*"\t", self.name, self.value))
        print("{}variable fields: \n".format(tab*"\t"))
        for field in self.fields:
            self.fields[field].show(tab+1)
        deps = self.getDependency()
        print("{}dependencies: {}".format(tab*"\t", list(deps.keys())))
        print("\n")
