from .grammar import Nonterminal, PProduction
from .semantics import Token, SemanticNonterminal, SemanticPCFG
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

class Expression(SemanticNonterminal):
    """Represents an expression of a particular type."""
    required_annotations = set(["datatype"])
    
    def __init__(self, datatype):
        super().__init__()
        self.datatype = datatype

        # if a datatype is not provided, it must be inferred later.
        if datatype is not None:
            self.annotations["datatype"] = datatype
    
    def annotate(self, scope: Scope):
        # TODO: infer expression types if/when it becomes useful.
        if "datatype" not in self.annotations:
            raise NotImplementedError()

    def __eq__(self, other):
        # Two expression symbols must be of the same datatype to be equal.
        return super().__eq__(other) and self.datatype == other.datatype
    
    def __hash__(self):
        # because we overload __eq__, we must overload __hash__ as well.
        return hash((super().__hash__(), self.datatype))
    
    def __str__(self):
        return f"Expression<{self.datatype}>"

########################################
#   Grammar                            #
########################################

expression_grammar = SemanticPCFG(
    Expression("Int"),
    [
        PProduction(Expression("Int"), (Int(), " + ", Expression("Int")), 0.1),
        PProduction(Expression("Int"), (Variable("Int"), " + ", Expression("Int")), 0.1),
        PProduction(Expression("Int"), (Int(), " * ", Expression("Int")), 0.1),
        PProduction(Expression("Int"), (Variable("Int"), " * ", Expression("Int")), 0.1),
        PProduction(Expression("Int"), (Int(),), 0.3),
        PProduction(Expression("Int"), (Variable("Int"),), 0.3),

        PProduction(Expression("Bool"), (Expression("Int"), " > ", Expression("Int")), 0.2),
        PProduction(Expression("Bool"), (Expression("Int"), " == ", Expression("Int")), 0.2),
        PProduction(Expression("Bool"), (Bool(),), 0.4),
    ]
)
