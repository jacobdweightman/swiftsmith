from .grammar import Nonterminal, PProduction
from .semantics import Token, SemanticPCFG

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
    """Represents a constant or variable which may appear in an expression."""
    def __init__(self, datatype, mutable=False):
        self.datatype = datatype
        self.mutable = mutable

    def string(self, scope):
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
        return f"Variable(datatype={self.datatype}, mutable={self.mutable})"

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
        PProduction(expression("Int"), (Variable("Int"), " + ", expression("Int")), 0.1),
        PProduction(expression("Int"), (Int(), " * ", expression("Int")), 0.1),
        PProduction(expression("Int"), (Variable("Int"), " * ", expression("Int")), 0.1),
        PProduction(expression("Int"), (Int(),), 0.3),
        PProduction(expression("Int"), (Variable("Int"),), 0.3),

        PProduction(expression("Bool"), (expression("Int"), " > ", expression("Int")), 0.2),
        PProduction(expression("Bool"), (expression("Int"), " == ", expression("Int")), 0.2),
        PProduction(expression("Bool"), (Bool(),), 0.4),
    ]
)
