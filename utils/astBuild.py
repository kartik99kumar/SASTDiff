from pycparser import parse_file


def makeAST(filename, mode):

    if mode == "line":

        filetmp = open("tmp/tmpcode", "w")
        fileorg = open(filename, "r")
        code = fileorg.read()
        fileorg.close()
        modcode = "void dummy(){{{}}}".format(code)
        filetmp.write(modcode)
        filetmp.close()
        filename = "tmp/tmpcode"

    ast = parse_file(filename)
    return ast
