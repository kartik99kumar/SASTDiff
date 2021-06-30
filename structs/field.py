class Field:

    def __init__(self, fieldName, object):
        self.name = fieldName
        self.structVariable = object

    def show(self):
        print("field name: {}".format(self.name))
