from structs.state import State
import process
import process.compound


def evaluateFuncDef(funcDef):

    state = State()

    if funcDef.decl.type.args is not None:

        args = funcDef.decl.type.args.params
        for arg in args:
            process.decl.evaluateDecl(arg, state)

    body = funcDef.body

    process.compound.evaluateCompound(body, state)

    return state
