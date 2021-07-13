# Static Application Security Testing Tool

## What is SAST Tool?

This tool is designed to find security vulnerabilities in C code. This is done by building an Abstract Syntax Tree of the C code. This is done through the open source library [pycparser](https://github.com/eliben/pycparser). The nodes of the trees are analysed to build a *state*. Appropriate scripts are run againts these states. After this analysis a report file is generated.

## What code can it analyze?

This tool is designed specifically for **C code**. Moreover the given code should be preprocessed. This is the prerequisite to parse the code using pycparser. More about preprocessing is given in [pycparser documentation](https://github.com/eliben/pycparser#using). For preprocessing simple codes, the following command can be used:

```bash
    gcc -E -Ifake_libc_include code.cpp -o preprocessedcode.cpp
```

The required *fake_libc_include* header files can be found [here](https://github.com/eliben/pycparser/tree/master/utils/fake_libc_include).

Any C code segments like lines of code or function definitions can also be analysed using this tool.

## Usage

1. Analysing full code or function definitions

    After preprocessing the code, run the script as:

```bash
    python3 src.py [filename]
```

2. Analysing lines of code

    Make sure there are no comments in the lines of code. Then run the script as:

```bash
    python3 src.py [filename] line
```

## Configuring the tool

The *config.json* file can be configured by the user to specify:

1. Allowed Addresses for Binding: This is used by the tool to find any binding call that may indicate binding to restricted addresses.
2. Validation Functions: These functions will be considered as validation functions for user inputs. This helps the tool to understand if the user inputs are validated or not.

## How the tool works?

1. ### Transforming the code into Abstract Syntax Tree

    The C code is transformed into an AST using [pycparser](https://github.com/eliben/pycparser) open source library. After parsing the code it returns the root node of the tree. Each node in the tree has its own class. The type of nodes and their attributes can be found [here](https://github.com/eliben/pycparser/blob/master/pycparser/c_ast.py). One example is Assignment node. The Assignment node class is as follows:

```python

    class Assignment(Node):
    __slots__ = ('op', 'lvalue', 'rvalue', 'coord', '__weakref__')
    def __init__(self, op, lvalue, rvalue, coord=None):
        self.op = op
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.coord = coord

    def children(self):
        nodelist = []
        if self.lvalue is not None: nodelist.append(("lvalue", self.lvalue))
        if self.rvalue is not None: nodelist.append(("rvalue", self.rvalue))
        return tuple(nodelist)

    def __iter__(self):
        if self.lvalue is not None:
            yield self.lvalue
        if self.rvalue is not None:
            yield self.rvalue

    attr_names = ('op', )

```

2. ### Analyzing these nodes in the tree to make Context

    To help make context of the nodes of the AST, we used three classes which provide structure:

    **Variable**
    : This class helps to maintain information about a variable in the code. This includes name, value, fields[for struct variables], dependencies and if the variable is user input or if the variable is validated or not. 

    **Call**
    : This class helps to maintain information about a function call that might occur in the code. It holds information about the function name, arguments which might either be constants or flags or variables, and the coordinates of the function call in the code. Note that the variable arguments are kept as the deepcopy of the original variables since they might change elsewhere in the code. 

    **State**
    : This class helps maintain information about a block in a code. It holds information about variables that are declared in the block or variables that can be accessed by the block (from the upper blocks), the function calls in the block, arguments/function parameters (if the block is a function) and its child blocks. The states are maintained as a tree with global state as the root.

3. ### Using security tools to analyze the State Tree

    The analysis tools take a State as the input and analyze primarily the function calls in the state. Another util class which is used is Warning class:

    **Warning**
    : This is a utility class that helps hold information about a vulnerability. This includes the type, message and coordinate.

    Each tool returns a list of Warning objects. 

    The State Tree is recursively analysed by all the tools and we get a list of Warning objects after the analysis. This list is sorted by coordinate and used to generate a report.

## Code Components 

1. structs/

    - [variable](https://github.com/kartik99kumar/SASTDiff/blob/master/structs/variable.py):

        - Class Variable:

            - name: name of the variable.
            - value: value of the variable. If no information about the value then it would be set to None.
            - fields: dictionary of fields of the variable (if variable is struct variable).
            - deps: dependencies including variables or function calls.
            - isInput: if the variable is user input or not. Initially set to False.
            - isValidated: if the variable is validated by a validation function or not. Initially set to False.
            - getValue(): returns variable value.
            - setValue(value): sets variable value to given value.
            - addField(fieldName): adds a field of the given name to the variable.
            - getField(fieldName): returns the reference to the field variable object.
            - getDependency(): returns the dictionary of all the dependencies of the variable. These include direct as well as indirect dependencies.
            - addDependency(dep): given dep (variable or call object) this adds its reference to variable dependencies.
            - resetDependencies(): clears the dependency dictionary.
            - setAsInput(): sets the isInput attribute to True.
            - setValidation(): sets the isValidated attribute to True.
            - resetValidation(): sets the isValidated attribute to False.
        
    - [call](https://github.com/kartik99kumar/SASTDiff/blob/master/structs/call.py):

        - Class Call:

            - name: name of the function call.
            - args: list of arguments of the function call. An argument can be constant or variable.
            - coord: coordinate of the function call in the code.
            - addArg(arg): appends the argument to the argument list.

    - [state](https://github.com/kartik99kumar/SASTDiff/blob/master/structs/state.py):

        - Class State:

            - variables: a dictionary of variables of the state (objects of class Variable).
            - args: a list of arguments of the state. This is used if the state block is a function definition.
            - calls: a list of function calls (object of class Call).
            - children: list of children states (objects of class State).
            - addVariable(variable): adds the given variable to the variables dictionary.
            - getVariable(variableName): returns the reference to the object of the variable with the name variableName if it exists in the state. Else it returns None.
            - addCall(call): appends the given call to the calls list.
            - getCall(callName): returns the list of calls with the given callName.
            - addArg(arg): appends the argument to the args list.
            - getArgs(): returns the args list.
            - snapshot(): returns the deepcopy of the state.
            - addStateVariables(state): adds the variables of the given state to the variables list of the current state. This is used to inherit variables from one state to another.
            - addChild(childState): appends the childState to children list.   

2. utils/

    - [astBuild](https://github.com/kartik99kumar/SASTDiff/blob/master/utils/astBuild.py):

        - makeAst(filename,mode): given the filename, it returns root node of the AST generated by the pycparser using the parse_file function. If the mode is *line* then the code is wrapped in a dummy container. The temp code is then fed into the parse_file function. The AST dump is written in *astdump.txt* file. It is to be noted any comments or preprocessor directives in the code breaks the parse_file code.

    - [table](https://github.com/kartik99kumar/SASTDiff/blob/master/utils/table.py): 

        - Class Visitor:

            - globalDeclarations: list of references to the nodes of global declarations.
            - functionDefinitions: dictionary of references to nodes of function definitions in the code.
            - visit_FuncDef(): visitor function which visits the function definition nodes and adds its reference to the functionDefinitions dictionary.
            - visit_Decl(): visitor function which visits declaration nodes in the global scope and adds its reference to the globalDeclarations list.

        - getDeclarations(root): given the root of the AST, it returns the list of global declarations nodes and function definition nodes.

        - makeTables(root): given the root of the AST, it returns the list of nodes of function definitions, nodes of struct definitions and nodes of global type declarations.

    - [data](https://github.com/kartik99kumar/SASTDiff/blob/master/utils/data.py):

        - Extracts the list of validation functions, allowed bind addresses etc. from the *config.json* file.
        - opens the *log.txt* file and *state.txt* file to store the logs and state tree.
    
    - [warning](https://github.com/kartik99kumar/SASTDiff/blob/master/utils/warning.py):

        - Class Warning:

            - coord: coordinate of vulnerability.
            - message: message of vulnerability.
            - type: type of vulnerability.

3. process/

    - [assignment](https://github.com/kartik99kumar/SASTDiff/blob/master/process/assignment.py):

        - evaluateAssignment(assignment, state): Given the reference of type assignment node of AST and a object reference of Class State, it does the following:

            - if the rvalue of the assignment is of type c_ast.ID, c_ast.StructRef and c_ast.Constant, it gets the value of this rvalue from the State. If there is no information about the value then value is taken as None.
            - if the lvalue is of type c_ast.ID or c_ast.StructRef then the value, dependency, validation of the variable is set appropriately in the State.

    - [code](https://github.com/kartik99kumar/SASTDiff/blob/master/process/code.py):

        - evaluateState(state): this function runs all the security tools on the given state and returns the list of Warning objects.

        - evaluateCode(filename, mode): this is the core function which calls *makeAST* to get root of the tree, *makeTables* to get function definition and global declaration list, makes a global state, adds the global variables to it, gets the state of all function definitions, evaluates all these states and generates the report using the list of Warning objects.

    - [compound](https://github.com/kartik99kumar/SASTDiff/blob/master/process/compound.py):

        - evaluateCompound(compound, parentState): Given the reference of type compound node and the reference of the parentState object, it does the following:

            - creates a state which of its own. It inherits the variables of its parent state.
            - evaluates each item like assignment, declaration, function call etc. in the block.
            - adds the created state as a child of the parent state.

    - [cond](https://github.com/kartik99kumar/SASTDiff/blob/master/process/cond.py):

        - evaluateCond(cond, state): Given an binary operator expression tree node, it evaluates each node. Specifically it looks if there is any function call in this expression tree and evaluates that function call node.

    - [decl](https://github.com/kartik99kumar/SASTDiff/blob/master/process/decl.py):

        - evaluateDecl(decl, state): Given the reference of type declaration node and the reference of the state object, it evaluates each declaration, creates its variable, sets its initial value and adds the variable to the state. It also sets any dependency if any.

    - [dowhileblock](https://github.com/kartik99kumar/SASTDiff/blob/master/process/dowhileblock.py):

        - evaluateDoWhile(doWhileBlock, state): Given the reference of type doWhile node and reference of the state object, it evaluates the condition of the block and evaluates the compound block of the doWhile.

    - [flags](https://github.com/kartik99kumar/SASTDiff/blob/master/process/flags.py):

        - evaluateFlags(arg, arglist): In certain function calls arguments are given as flags/modes which are ORed together. This function evaluates those flags individually and adds those to the reference of the list arglist given.

    - [forblock](https://github.com/kartik99kumar/SASTDiff/blob/master/process/forblock.py):

        - evaluateFor(forBlock, state): Given the reference of type For node and reference of the state object, it evaluates the condition of the block and evaluates the compound block of the For.

    - [funccall](https://github.com/kartik99kumar/SASTDiff/blob/master/process/funccall.py):

        - evaluateFuncCall(funcCall, state): Given the reference of type FuncCall node and reference of the state object, it evaluates the FuncCall node as follows:

            - it creates a Call object with the function name and coordinate extracted from the node.
            - it then evaluates each of the argument in the args list of the function call and adds each argument's deepcopy to the call object.
            - argument variable's isInput and isValidated is set appropriately.
            - if the function is a modifier function, evaluateModFunc is called.
            - this call object is added to the state.

    - [funcdef](https://github.com/kartik99kumar/SASTDiff/blob/master/process/funcdef.py):

        - evaluateFuncDef(funcDef, parentState): Given the reference of type funcDef node and the reference of the state object, it does the following:

            - creates a new state. Inherits variables from the parentState.
            - it adds arguments of the function to the state.
            - it evaluates the body block/compound of the function definition.
            - the state is added as a child to the parentState.

    - [ifblock](https://github.com/kartik99kumar/SASTDiff/blob/master/process/ifblock.py):

        - evaluateIf(ifBlock, state): Given the reference of type If node and the reference of the state object this function evaluates the condition of the If block as well as the compound body.

    - [modfunc](https://github.com/kartik99kumar/SASTDiff/blob/master/process/modfunc.py):

        -evaluateModFunc(funcCall, state): Given the reference of the Call object and the reference of the state object, this function adds additional dependencies to the variables. Function calls like strcpy, sprintf, strcat etc. add additional dependencies to variables. These are added by calling this function.

    - [ret](https://github.com/kartik99kumar/SASTDiff/blob/master/process/ret.py):

        -evaluateReturn(ret, state): Given the reference of type Return node and reference of the state object, this function returns the reference of the variable returned by the function definition.

    - [structref](https://github.com/kartik99kumar/SASTDiff/blob/master/process/structref.py):

        -evaluateStructRef(ref, state): Given the reference of type StructRef node and reference of the state object, this function returns the reference of the field variable. For example if the struct reference is a.b.c.d, then the reference to the variable field d is return by this function.

    - [whileblock](https://github.com/kartik99kumar/SASTDiff/blob/master/process/whileblock.py):

        - evaluateWhile(whileBlock, state): Given the reference of type While node and reference of the state object, this function evaluates the condition of the while block and evaluates the body/compound of the while block.

4. tools/

    - [bind](https://github.com/kartik99kumar/SASTDiff/blob/master/tools/bind.py):

        - evaluateBind(state): this function analyzes the *bind* calls in the given state. The second argument is the object of struct sockaddr. This function analyzes this object. It ensures that the bind address is not:

            - INADDR_ANY: When INADDR_ANY is specified in the bind call, the socket will be bound to all local interfaces. It doesn't care about the address.
            - any address that is not allowed (in the config file).

    - [buffer](https://github.com/kartik99kumar/SASTDiff/blob/master/tools/buffer.py):

        - evaluateBufferOverflow(state): this function analyzes the input calls which don't take buffer size as argument. This may cause buffer overflow. These calls include gets, strcat, strcpy and scanf, fscanf, sprintf, sscanf with no buffer sizes mentioned in the formatted strings ("%9s" for example).

    - [certverify](https://github.com/kartik99kumar/SASTDiff/blob/master/tools/certverify.py):

        - evaluateCertificates(state): this function analyzes OpenSSL certificate validation. Validation of certificates is essential to create secure SSL/TLS sessions not vulnerable to man-in-the-middle attacks. The second argument of the *SSL_CTX_set_verify* should be *SSL_VERIFY_PEER* and this function should not use custom validation callbacks as they are not recommended.

    - [filepermission](https://github.com/kartik99kumar/SASTDiff/blob/master/tools/filepermission.py):

        - evaluateBadFilePermission(state): this function flags any *chmod* function calls that changes the permission of a file to write/execute by group/others.

    - [securepadding](https://github.com/kartik99kumar/SASTDiff/blob/master/tools/securepadding.py):

        - evaluatePadding(state): in OpenSSL, for RSA encryption algorithm, the recommended padding scheme is OAEP. This function analyzes *RSA_public_decrypt* call for this.

    - [serverhostverify](https://github.com/kartik99kumar/SASTDiff/blob/master/tools/serverhostverify.py):

        - evaluateHostVerify(state): OpenSSL provides built-in hostname verification functions that should be used to prevent man in middle attacks. This function analyzes *SSL_set1_host* call to ensure this.

    - [shell](https://github.com/kartik99kumar/SASTDiff/blob/master/tools/shell.py):

        - evaluateShell(state): this function checks for shell injection vulnerability. It analyzes *system* and *popen* calls to check if the input to these functions is a user input or has any user input dependency.

## Project Scope and Further Development

1. Evaluating AST Components

    The component evaluation scripts as of now focus on the most common coding pratices and syntax. More rules might be added as the tool is developed. For instance switch-case, ternary operator etc. scripts can be added. Evaluation of function calls as arguments, more popular modification functions may also be added.

2. More Security Tools

    The analysis of a code can easily be done through the analysis of State object. The current security tools may be improved by adding more vulnerable patterns. One popular resource with good security vulnerability patterns that might be used to add and improve the tool can be found [here](https://rules.sonarsource.com/c). More specific tools related to any proprietary library can also be easily added.


        



