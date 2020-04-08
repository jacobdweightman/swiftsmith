from .access import AccessModifier
from .formatting import EOL
from .grammar import Nonterminal, PProduction
from .names import identifier
from .semantics import Token, SemanticNonterminal, SemanticParseTree, SemanticPCFG
from .scope import Scope
from .types import AccessLevel, EnumType

import random

########################################
#   Tokens                             #
########################################

class Enum(Token):
    required_annotations = set(["name", "type"])

    def annotate(self, scope: Scope, context: SemanticParseTree):
        access = context.parent.value.annotations["access"]
        name = next(identifier).capitalize()
        self.annotations["name"] = name

        datatype = EnumType(name, access=access)
        self.annotations["type"] = datatype

        next_scope = Scope(parent=scope)
        next_scope.value = datatype
        scope.add_child(next_scope)
        scope.next_scope = scope.children[-1]

        def closure():
            scope.next_scope = scope
        context.parent.childwhere(lambda n: n.value == statements).defer(closure)

    def string(self):
        assert self.is_annotated()
        return self.annotations["name"]


class Case(Token):
    required_annotations = set(["name", "associatedvalues"])

    def annotate(self, scope: Scope, context: SemanticParseTree):
        assert isinstance(scope.value, EnumType)
        access = scope.value.access
        name = next(identifier)
        self.annotations["name"] = name

        # TODO: handle recursive ("indirect") enums.
        # An associated value's type cannot be less visible than the enum. For instance,
        # a public enum cannot have a case with a private associated value.
        types = scope.accessible_types(at_least=scope.value.access)
        assert scope.value not in types
        try:
            associatedvalues = [random.choice(types) for _ in range(random.randint(0, 1))]
            associatedvalues = [scope.specialize_type(t, at_least=access) for t in associatedvalues]
        except IndexError:
            associatedvalues = []
        self.annotations["associatedvalues"] = associatedvalues

        scope.value.add_case(name, associatedvalues)
    
    def string(self):
        assert self.is_annotated()
        associatedvalues = self.annotations["associatedvalues"]
        if len(associatedvalues) > 0:
            avstr = "(" + ", ".join(av.full_name() for av in associatedvalues) + ")"
        else:
            avstr = ""
        return self.annotations["name"] + avstr

########################################
#   Nonterminals                       #
########################################

class EnumDeclaration(SemanticNonterminal):
    """
    Represents a complete enum declaration in Swift.
    
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

statements = Nonterminal("ENUM_STATEMENTS")
statement = Nonterminal("ENUM_STATEMENT")

########################################
#   Grammar                            #
########################################

enum_grammar = SemanticPCFG(
    EnumDeclaration(),
    [
        PProduction(EnumDeclaration(), (EOL(), EOL(), AccessModifier(), "enum ", Enum(), ": Hashable {", statements, EOL(), "}"), 1.0),
        PProduction(statements, (statement, statements), 0.5),
        PProduction(statements, (statement,), 0.5),
        PProduction(statement, (EOL(), "case ", Case()), 1.0)
    ]
)
