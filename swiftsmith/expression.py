from .grammar import Nonterminal, PProduction
from .semantics import Token, SemanticPCFG
from .scope import Scope

import random

########################################
#   Tokens                             #
########################################

class Int(Token):
    """Represents an integer literal token."""
    required_annotations = set(["value"])

    def annotate(self, scope: Scope):
        self.annotations["value"] = random.randint(0, 5)
    
    def string(self):
        assert self.is_annotated()
        return str(self.annotations["value"])

    def __str__(self):
        return "Int()"


class Bool(Token):
    """Represents a boolean literal token."""
    required_annotations = set(["value"])

    def annotate(self, scope: Scope):
        self.annotations["value"] = random.choice(["true", "false"])
    
    def string(self):
        assert self.is_annotated()
        return self.annotations["value"]

    def __str__(self):
        return "Bool()"


class Variable(Token):
    """Represents a constant or variable which may appear in an expression."""
    required_annotations = set(["value"])
    def __init__(self, datatype, mutable=False):
        super().__init__()
        self.datatype = datatype
        self.mutable = mutable

    def annotate(self, scope: Scope):
        try:
            self.annotations["value"] = scope.choose_variable(datatype=self.datatype, mutable=self.mutable)
        except IndexError:
            if self.datatype == "Int":
                substitute = Int()
            elif self.datatype == "Bool":
                substitute = Bool()
            else:
                raise ValueError(f"Cannot construct literal of type `{self.datatype}`")
            substitute.annotate(scope)
            self.annotations["value"] = substitute.string()

    def string(self):
        assert self.is_annotated()
        return self.annotations["value"]
    
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
