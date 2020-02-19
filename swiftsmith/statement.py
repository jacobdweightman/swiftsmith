from .grammar import Nonterminal, PProduction
from .expression import expression
from .formatting import EOL
from .scope import Scope
from .semantics import Token, SemanticPCFG
from .names import identifier

########################################
#   Tokens                             #
########################################

class Declaration(Token):
    """
    Represents the declaration of a constant or variable which would appear on the left
    side of an assignment.
    """
    required_annotations = set(["name"])

    def __init__(self, datatype, mutable=False):
        super().__init__()
        self.datatype = datatype
        self.mutable = mutable

    def annotate(self, scope: Scope):
        name = next(identifier)

        # This name isn't usable in a declaration with an initial value. We defer
        # adding this variable to the scope until after it is declared.
        closure = (lambda: scope.declare(name, self.datatype, self.mutable))
        scope.defer(closure)

        self.annotations["name"] = name
    
    def string(self):
        assert self.is_annotated()
        mutability = "var " if self.mutable else "let "
        return mutability + self.annotations["name"]
    
    def __str__(self):
        mutability = "var" if self.mutable else "let"
        return f"DECLARATION<{mutability}, {self.datatype}>"

########################################
#   Nonterminals                       #
########################################

statement = Nonterminal("STATEMENT")
assignment = Nonterminal("ASSIGNMENT")
declaration = Nonterminal("DECLARATION")

########################################
#   Grammar                            #
########################################

statement_grammar = SemanticPCFG(
    assignment,
    [
        PProduction(assignment, (EOL(), Declaration("Int"), " = ", expression("Int")), 0.3),
        PProduction(assignment, (EOL(), Declaration("Int", mutable=True), " = ", expression("Int")), 0.3),
        #PProduction(assignment, (EOL(), Variable("Int"), " = ", expression("Int")), 0.7),
    ]
)