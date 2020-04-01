from .grammar import Nonterminal, PProduction
from .expression import Expression
from .formatting import EOL
from .scope import Scope
from .semantics import Token, SemanticPCFG, SemanticParseTree, SemanticNonterminal
from .names import identifier
from .types import DataType
from .standard_library import Int

########################################
#   Tokens                             #
########################################

class Declaration(Token):
    """
    Represents the declaration of a constant or variable which would appear on the left
    side of an assignment.
    """
    required_annotations = set(["name", "datatype"])

    def __init__(self, datatype, mutable=False):
        super().__init__()
        self.mutable = mutable
        self.datatype = datatype

    def annotate(self, scope: Scope, context: SemanticParseTree):
        name = next(identifier)

        if self.datatype is None:
            self.datatype = scope.choose_type()
        # pass the type along to the parent assignment, so that the expression on the
        # right side of this assignment can infer its type.
        context.parent.value.datatype = self.datatype

        # This name isn't usable in its own initial value. We defer adding this
        # variable to the scope until after it is initalized.
        closure = (lambda: scope.declare(name, self.datatype, self.mutable))
        context.parent.defer(closure)

        self.annotations["name"] = name
        self.annotations["datatype"] = self.datatype
    
    def string(self):
        assert self.is_annotated()
        mutability = "var " if self.mutable else "let "
        return mutability + self.annotations["name"]
    
    def __str__(self):
        mutability = "var" if self.mutable else "let"
        return f"DECLARATION<{mutability}, {self.datatype}>"

class Variable(Token):
    """Represents a variable as it would appear in an assignment."""
    required_annotations = {"name"}

    def __init__(self, datatype):
        super().__init__()
        self.datatype = datatype
    
    def annotate(self, scope: Scope, context: SemanticParseTree):
        try:
            variable = scope.choose_variable(datatype=self.datatype, mutable=True)
        except IndexError:
            # fall back to declaring a new variable
            declaration = Declaration(self.datatype, mutable=True)
            declaration.annotate(scope, context)
            self.annotations["name"] = declaration.string()
            return
        
        # pass the type along to the parent assignment, so that the expression on the
        # right side of this assignment can infer its type.
        context.parent.value.datatype = variable.datatype

        self.annotations["name"] = variable.name

    def string(self):
        assert self.is_annotated()
        return self.annotations["name"]

########################################
#   Nonterminals                       #
########################################

class Assignment(SemanticNonterminal):
    """
    Represents a statement which assigns a value to a variable.

    It will likely be useful later to be able to specify the type of an assignment, for
    instance in a metamorphic relation. In the meantime, passing `None` into `datatype`
    will determine the type at annotation time. The variable and expression's types are
    inferred either way.
    """
    def __init__(self, datatype: DataType):
        super().__init__()
        self.datatype = datatype
    
    def annotate(self, scope: Scope, context: SemanticParseTree):
        #assert self.datatype is not None, "assignment statement was not given a type."
        pass
    
    # By not overloading __eq__ and __hash__, assignments with different types compare
    # as equal and share productions in the grammar.
    
    #def __eq__(self, other):
        #return return super().__eq__(other) and self.datatype == other.datatype
    
    #def __hash__(self):
        #return hash((super().__hash__(), self.datatype))
    
    def __str__(self):
        return f"assignment<{self.datatype}>"
    
    def __repr__(self):
        return f"assignment<{self.datatype}>"

class DeclarationAssignment(Assignment):
    """Represents a declaration of a new variable, which may occur at file scope."""
    pass

statement = Nonterminal("STATEMENT")
declaration = Nonterminal("DECLARATION")

########################################
#   Grammar                            #
########################################

statement_grammar = SemanticPCFG(
    Assignment(None),
    [
        PProduction(DeclarationAssignment(None), (EOL(), Declaration(None), " = ", Expression(None)), 0.7),
        PProduction(DeclarationAssignment(None), (EOL(), Declaration(None, mutable=True), " = ", Expression(None)), 0.3),
        PProduction(Assignment(None), (EOL(), Variable(None), " = ", Expression(None)), 0.7),
        PProduction(Assignment(None), (DeclarationAssignment(None),), 0.3),
    ]
)
