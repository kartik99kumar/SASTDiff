class Warning:

    def __init__(self, coord, message, type):

        self.coord = coord
        self.message = message
        self.type = type

    def show(self, file=None):

        wstr = "{}: {} warning: \n\t{}\n\n".format(
            self.coord, self.type, self.message)

        if file is not None:
            file.write(wstr)
