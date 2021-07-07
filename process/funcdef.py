from structs.state import State
import process
import process.compound


def evaluateFuncDef(funcDef, parentState):

    state = State()
    state.addStateVariables(parentState)

    if funcDef.decl.type.args is not None:

        args = funcDef.decl.type.args.params
        for arg in args:
            process.decl.evaluateDecl(arg, state)

    body = funcDef.body

    process.compound.evaluateCompound(body, state)

    parentState.addChild(state)
