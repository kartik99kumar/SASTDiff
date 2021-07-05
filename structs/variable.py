class Variable:

    def __init__(self, name):
        self.name = name
        self.value = None
        self.fields = {}
        self.deps = {}
        self.isInput = False
        self.isValidated = False

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

    def setValidation(self):
        self.isValidated = True

    def resetValidation(self):
        self.isValidated = False

    def show(self, tab=0):

        varstr = ""
        varstr += "{}variable name: {} value: {}\n".format(
            tab*"\t", self.name, self.value)
        varstr += "{}user input: {} validation: {}\n".format(
            tab*"\t", self.isInput, self.isValidated)
        varstr += "{}variable fields: \n\n".format(tab*"\t")
        for field in self.fields:
            varstr += self.fields[field].show(tab+1)
        deps = self.getDependency()
        varstr += "{}dependencies: {}\n".format(tab*"\t", list(deps.keys()))
        varstr += "\n"

        return varstr
