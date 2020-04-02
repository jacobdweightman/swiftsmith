from .formatting import EOL
from .grammar import Nonterminal, PProduction
from .names import identifier
from .semantics import Token, SemanticParseTree, SemanticPCFG
from .scope import Scope
from .types import EnumType

import random

########################################
#   Tokens                             #
########################################

class Enum(Token):
    required_annotations = set(["name", "type"])

    def annotate(self, scope: Scope, context: SemanticParseTree):
        name = next(identifier).capitalize()
        self.annotations["name"] = name

        datatype = EnumType(name)
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
        name = next(identifier)
        self.annotations["name"] = name

        # TODO: handle recursive ("indirect") enums.
        types = scope.accessible_types()
        types.remove(scope.value)
        assert scope.value not in types
        try:
            associatedvalues = [random.choice(types) for _ in range(random.randint(0, 1))]
        except IndexError:
            associatedvalues = []
        self.annotations["associatedvalues"] = associatedvalues

        scope.value.add_case(name, associatedvalues)
    
    def string(self):
        assert self.is_annotated()
        associatedvalues = self.annotations["associatedvalues"]
        if len(associatedvalues) > 0:
            avstr = "(" + ", ".join(av.name for av in associatedvalues) + ")"
        else:
            avstr = ""
        return self.annotations["name"] + avstr

########################################
#   Nonterminals                       #
########################################

enum = Nonterminal("ENUM")
statements = Nonterminal("ENUM_STATEMENTS")
statement = Nonterminal("ENUM_STATEMENT")

########################################
#   Grammar                            #
########################################

enum_grammar = SemanticPCFG(
    enum,
    [
        PProduction(enum, (EOL(), EOL(), "enum ", Enum(), " {", statements, EOL(), "}"), 1.0),
        PProduction(statements, (statement, statements), 0.5),
        PProduction(statements, (statement,), 0.5),
        PProduction(statement, (EOL(), "case ", Case()), 1.0)
    ]
)
