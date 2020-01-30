from .grammar import Nonterminal, PProduction
from .semantics import Token, SemanticPCFG
from .names import identifier

import random

########################################
#   Tokens                             #
########################################

class Int(Token):
    """Represents an integer literal token."""
    def string(self, scope):
        return str(random.randint(0, 5))

    def __str__(self):
        return "Int()"


class Bool(Token):
    """Represents a boolean literal token."""
    def string(self, scope):
        return random.choice(["true", "false"])

    def __str__(self):
        return "Bool()"


class Variable(Token):
    """Represents a Swift variable token."""
    def __init__(self, datatype=None, declaration=False, mutable=False):
        self.datatype = datatype
        self.declaration = declaration
        self.mutable = mutable

    def string(self, scope):
        if self.declaration:
            name = next(identifier)

            # This name isn't usable in a declaration with an initial value. We defer
            # adding this variable to the scope until after it is declared.
            closure = (lambda: scope.declare(name, "Int", self.mutable))
            scope.defer(closure)

            return name
        else:
            if scope.variables:
                return scope.choose_variable()
            else:
                # if there are no variables of the correct type in scope, fall back to a
                # literal value.
                if self.datatype == "Int":
                    return Int().string(scope)
                elif self.datatype == "Bool":
                    return Bool().string(scope)
                else:
                    raise ValueError(f"Cannot construct literal of type `{self.datatype}`")
    
    def __str__(self):
        return f"Variable(datatype={self.datatype}, declaration={self.declaration}, mutable={self.mutable})"

########################################
#   Nonterminals                       #
########################################

def expression(t):
    """Represents an expression that resolves to a value of type `t`."""
    return Nonterminal(f"EXPRESSION<{t}>")

########################################
#   Grammar                            #
########################################

expression_grammar = SemanticPCFG(
    expression("Int"),
    [
        PProduction(expression("Int"), (Int(), " + ", expression("Int")), 0.1),
        PProduction(expression("Int"), (Variable(datatype="Int"), " + ", expression("Int")), 0.1),
        PProduction(expression("Int"), (Int(), " * ", expression("Int")), 0.1),
        PProduction(expression("Int"), (Variable(datatype="Int"), " * ", expression("Int")), 0.1),
        PProduction(expression("Int"), (Int(),), 0.3),
        PProduction(expression("Int"), (Variable(datatype="Int"),), 0.3),

        PProduction(expression("Bool"), (expression("Int"), " > ", expression("Int")), 0.2),
        PProduction(expression("Bool"), (expression("Int"), " == ", expression("Int")), 0.2),
        PProduction(expression("Bool"), (Bool(),), 0.4),
    ]
)
