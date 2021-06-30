# makes global variable table, function definition and structure table

import pycparser.c_ast as ast
from pycparser.c_ast import NodeVisitor


class Visitor(NodeVisitor):

    def __init__(self):
        self.globalDeclarations = []
        self.functionDefinitions = {}

    def visit_FuncDef(self, node):
        name = node.decl.name
        if name is not None:
            self.functionDefinitions[name] = node

    def visit_Decl(self, node):
        self.globalDeclarations.append(node)


def getDeclarations(root):
    v = Visitor()
    v.visit(root)
    return v.globalDeclarations, v.functionDefinitions


def makeTables(root):

    globalDecls, funcDefs = getDeclarations(root)
    funcTable = funcDefs

    structTable = {}
    globalVarTable = {}

    for decl in globalDecls:
        if(isinstance(decl.type, ast.Struct)):
            structTable[decl.type.name] = decl.type
        elif(isinstance(decl.type, (ast.TypeDecl, ast.ArrayDecl, ast.PtrDecl))):
            globalVarTable[decl.name] = decl

    return funcTable, structTable, globalVarTable
