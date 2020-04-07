from .access import AccessModifier
from .grammar import Nonterminal, PProduction
from .scope import Scope
from .branch import branch_statement
from .expression import Expression
from .formatting import EOL, Block
from .statement import Assignment
from .semantics import Token, PCFG, SemanticParseTree, SemanticNonterminal
from .names import identifier
from .standard_library import Int
from .types import AccessLevel

import random

########################################
#   Tokens                             #
########################################

class Function(Token):
    """Represents a function signature as it appears in a function declaration."""
    required_annotations = set(["name", "arguments", "returntype"])

    def annotate(self, scope: Scope, context: SemanticParseTree):
        access = context.parent.value.annotations["access"]
        self.annotations["name"] = next(identifier)

        # A function cannot be more visible than the types in its signature. For
        # example, a public function cannot return a private type. In practice,
        # there should always be at least one because of the Standard Library.
        candidate_types = scope.accessible_types(at_least=access)

        arguments = {}
        for _ in range(random.randint(1, 3)):
            argtype = scope.specialize_type(
                random.choice(candidate_types),
                at_least=access
            )
            arguments[next(identifier)] = argtype
        self.annotations["arguments"] = arguments

        # TODO: allow non-Int return types
        returntype = scope.specialize_type(
            random.choice(candidate_types),
            at_least=access
        )
        self.annotations["returntype"] = returntype
        context.parent.value.datatype = returntype

        def declare_func():
            scope.declare_func(
                access,
                self.annotations["name"],
                self.annotations["arguments"],
                self.annotations["returntype"]
            )
        context.parent.defer(declare_func)

        def closure():
            for argument, datatype in arguments.items():
                scope.children[-1].declare(argument, datatype, False)
        context.parent.childwhere(lambda n: n.value == block).children[0].defer(closure)
    
    def string(self):
        assert self.is_annotated()
        name = self.annotations["name"]
        arguments = self.annotations["arguments"]
        returntype = self.annotations["returntype"]

        argstring = ', '.join(k + ": " + v.full_name() for (k,v) in arguments.items())
        
        return f"{name}({argstring}) -> {returntype.full_name()}"

########################################
#   Nonterminals                       #
########################################

class FuncDeclaration(SemanticNonterminal):
    """
    Represents a complete function declaration in Swift.
    
    By default, its access level is internal, but the access level may be overridden by
    modifying its "access" annotation via the `annotate` method of another node in the
    parse tree.

    Specifying the access level sets the "locked" annotation which suggests to other
    nodes in the parse tree that they should not modify the access level.
    """
    required_annotations = {"access", "locked"}

    def __init__(
        self,
        access: AccessLevel=None,
        default_access: AccessLevel=AccessLevel.internal
    ):
        super().__init__()
        self.datatype = None
        if access is not None:
            self.annotations["locked"] = True
            self.annotations["access"] = access
        else:
            self.annotations["locked"] = False
            self.annotations["access"] = default_access
    
    def annotate(self, scope: Scope, context: SemanticParseTree):
        pass


block = Nonterminal("FUNC_BLOCK")
statements = Nonterminal("FUNC_STATEMENTS")
statement = Nonterminal("FUNC_STATEMENT")

########################################
#   Grammar                            #
########################################

function_grammar = PCFG(
    FuncDeclaration(),
    [
        PProduction(FuncDeclaration(), (EOL(), EOL(), AccessModifier(), "func ", Function(), " {", block, EOL(), "}"), 1.0),
        PProduction(block, (Block(), statements), 1.0),

        PProduction(statements, (statement, statements), 0.7),
        PProduction(statements, (EOL(), "return ", Expression(None)), 0.3),
        PProduction(statement, (Assignment(None),), 0.7),
        PProduction(statement, (branch_statement,), 0.3)
    ]
)
