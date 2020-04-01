from .grammar import Nonterminal, PProduction
from .semantics import Token, SemanticNonterminal, SemanticParseTree
from .scope import Scope
from .types import CallSyntax, DataType, EnumType

import random

########################################
#   Tokens                             #
########################################

class Value(Token):
    """
    Represents a value of a type.
    
    This may be a literal, an enum case, or a constructor call, depending on the type
    that it represents.
    """
    required_annotations = {"value"}

    def __init__(self, datatype: DataType):
        assert datatype is not None
        super().__init__()
        self.datatype = datatype
    
    def annotate(self, scope: Scope, context: SemanticParseTree):
        self.annotations["value"] = self.datatype.newvalue()
    
    def string(self):
        return self.annotations["value"]
    
    def __str__(self):
        return f"Value<{self.datatype}>"


class Variable(Token):
    """Represents a constant or variable which may appear in an expression."""
    required_annotations = set(["value"])
    def __init__(self, datatype, mutable=False):
        super().__init__()
        self.datatype = datatype
        self.mutable = mutable

    def annotate(self, scope: Scope, context: SemanticParseTree):
        try:
            self.annotations["value"] = scope.choose_variable(datatype=self.datatype, mutable=self.mutable).name
        except IndexError:
            self.annotations["value"] = self.datatype.newvalue()

    def string(self):
        assert self.is_annotated()
        return self.annotations["value"]
    
    def __str__(self):
        return f"Variable(datatype={self.datatype}, mutable={self.mutable})"


class Expression(Token):
    """Represents an expression of a particular type."""
    required_annotations = set(["datatype", "subtree"])
    
    def __init__(self, datatype: DataType):
        super().__init__()
        self.datatype = datatype

        # if a datatype is not provided, it must be inferred later.
        if datatype is not None:
            self.annotations["datatype"] = datatype
    
    def annotate(self, scope: Scope, context: SemanticParseTree):
        if "datatype" not in self.annotations:
            # Currently, type inference on expressions is only used with assignments.
            # Reading the type off of the parent node is adequate for now.
            self.datatype = context.parent.value.datatype
            self.annotations["datatype"] = self.datatype
        
        if random.random() < 0.5:
            if random.random() < 0.7:
                tree = SemanticParseTree(Variable(self.datatype))
            else:
                tree = SemanticParseTree(Value(self.datatype))
        else:
            # generate function call
            # Note: we currently only allow an expression to contain a single function
            # call. this produces simpler expressions and guarantees that expression
            # generation halts.
            try:
                fname, ftype = scope.choose_function(returntype=self.datatype)
                tree = SemanticParseTree(FunctionCall(fname, ftype), [])
            except IndexError:
                tree = SemanticParseTree(Variable(self.datatype))
        
        tree.annotate(scope=scope)
        self.annotations["subtree"] = tree
    
    def string(self):
        assert self.is_annotated()
        return self.annotations["subtree"].string()

    def __eq__(self, other):
        # Two expression symbols must be of the same datatype to be equal.
        return self.__class__ == other.__class__ and \
               super().__eq__(other) and \
               self.datatype == other.datatype
    
    def __hash__(self):
        # because we overload __eq__, we must overload __hash__ as well.
        return hash((super().__hash__(), self.datatype))
    
    def __str__(self):
        return f"Expression<{self.datatype}>"

    def __repr__(self):
        return f"Expression<{self.datatype}>"

########################################
#   Nonterminals                       #
########################################

class FunctionCall(SemanticNonterminal):
    """
    Represents a function call.

    This is a hack due to the variety of function call syntaxes in Swift. As a result,
    the "parse tree" it works with is slightly abstracted from the actual text that it
    generates, so strictly speaking it's an AST and not a parse tree. In order to
    generate the correct syntax, `annotate` modifies the tree by creating its own 
    children which is typically not recommended. Usage of this class:
    ```
    tree = SemanticParseTree(FunctionCall(Int), []) # explicitly pass empty children
    tree.annotate()
    print(tree.string())
    ```
    """
    def __init__(self, name, functiontype):
        super().__init__()
        self.name = name
        self.functiontype = functiontype

    def annotate(self, scope: Scope, context: SemanticParseTree):
        name = self.name
        ftype = self.functiontype

        if ftype.syntax == CallSyntax.normal:
            children = [name, "("]
            for argname, argtype in ftype.arguments.items():
                children.append(f"{argname}: ")
                children.append(Variable(argtype))
                children.append(", ")
            children[-1] = ")"
        elif ftype.syntax == CallSyntax.prefix:
            argtype = list(ftype.arguments.values())[0]
            children = [name, Variable(argtype)]
        elif ftype.syntax == CallSyntax.infix:
            argtype1, argtype2 = list(ftype.arguments.values())
            children = [Variable(argtype1), " ", name, " ", Variable(argtype2)]
        elif ftype.syntax == CallSyntax.postfix:
            argtype = list(ftype.arguments.values())[0]
            children = [Variable(argtype), name]
        else:
            raise NotImplementedError(ftype.syntax)

        context.children = list(map(SemanticParseTree, children))
