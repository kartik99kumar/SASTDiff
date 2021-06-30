from structs.variable import Variable


class StructVariable:

    def __init__(self, name, structureName):
        self.name = name
        self.structureName = structureName
        self.fields = {}

    def getFieldValue(self, fieldName):
        if fieldName in self.fields:
            return self.fields[fieldName].getValue()
        else:
            return None

    def updateFieldValue(self, fieldName, newValue):
        if fieldName not in self.fields:
            var = Variable(fieldName)
            self.fields[fieldName] = var
        self.fields[fieldName].updateValue(newValue)

    def addFieldDependency(self, fieldName, dependency):
        if fieldName in self.fields:
            self.fields[fieldName].addDependency(dependency)

    def resetFieldDependency(self, fieldName):
        if fieldName in self.fields:
            self.fields[fieldName].resetDependency()

    def show(self):
        print("name: {} structure name: {}".format(
            self.name, self.structureName))
        print("fields:")
        for field in self.fields:
            self.fields[field].show()
