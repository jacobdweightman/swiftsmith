from .grammar import Nonterminal, PProduction
from .semantics import Token, SemanticNonterminal, SemanticParseTree, SemanticPCFG
from .scope import Scope
from .types import DataType, Int, Bool

import random

########################################
#   Tokens                             #
########################################

class IntLiteral(Token):
    """Represents an integer literal token."""
    required_annotations = set(["value"])

    def annotate(self, scope: Scope, context: SemanticParseTree):
        self.annotations["value"] = random.randint(0, 5)
    
    def string(self):
        assert self.is_annotated()
        return str(self.annotations["value"])

    def __str__(self):
        return "Int()"


class BoolLiteral(Token):
    """Represents a boolean literal token."""
    required_annotations = set(["value"])

    def annotate(self, scope: Scope, context: SemanticParseTree):
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

    def annotate(self, scope: Scope, context: SemanticParseTree):
        try:
            self.annotations["value"] = scope.choose_variable(datatype=self.datatype, mutable=self.mutable)
        except IndexError:
            if self.datatype == Int:
                substitute = IntLiteral()
            elif self.datatype == Bool:
                substitute = BoolLiteral()
            else:
                raise ValueError(f"Cannot construct literal of type `{self.datatype}`")
            substitute.annotate(scope, context)
            self.annotations["value"] = substitute.string()

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
        
        subtree = _expression_grammar.randomtree(start=expression(self.datatype))
        subtree.annotate(scope=scope)
        self.annotations["subtree"] = subtree
    
    def string(self):
        assert self.is_annotated()
        return self.annotations["subtree"].string()

    def __eq__(self, other):
        # Two expression symbols must be of the same datatype to be equal.
        return super().__eq__(other) and self.datatype == other.datatype
    
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

def expression(datatype) -> Nonterminal:
    return Nonterminal(f"expression<{datatype}>")

########################################
#   Grammar                            #
########################################

_expression_grammar = SemanticPCFG(
    expression(Int),
    [
        PProduction(expression(Int), (IntLiteral(), " + ", expression(Int)), 0.1),
        PProduction(expression(Int), (Variable(Int), " + ", expression(Int)), 0.1),
        PProduction(expression(Int), (IntLiteral(), " * ", expression(Int)), 0.1),
        PProduction(expression(Int), (Variable(Int), " * ", expression(Int)), 0.1),
        PProduction(expression(Int), (IntLiteral(),), 0.3),
        PProduction(expression(Int), (Variable(Int),), 0.3),

        PProduction(expression(Bool), (expression(Int), " > ", expression(Int)), 0.2),
        PProduction(expression(Bool), (expression(Int), " == ", expression(Int)), 0.2),
        PProduction(expression(Bool), (BoolLiteral(),), 0.4),
    ]
)
