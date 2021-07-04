from pycparser import parse_file


def makeAST(filename):
    ast = parse_file(filename)
    return ast
