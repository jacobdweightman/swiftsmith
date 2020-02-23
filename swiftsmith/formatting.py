from .grammar import Nonterminal
from .scope import Scope
from .semantics import Token, SemanticParseTree

########################################
#   Tokens                             #
########################################

class Block(Token):
    def __init__(self, returntype=None):
        self.returntype = returntype
    
    def annotate(self, scope: Scope, context: SemanticParseTree):
        # "push" a new scope nested in the current one
        scope.children.append(Scope(parent=scope))
        scope.next_scope = scope.children[-1]

        def closure():
            # "pop" the scope once its content has been generated
            scope.next_scope = scope
        context.parent.defer(closure)
    
    def string(self):
        return ""
    
    def __str__(self):
        return f"Block({self.returntype or ''})"


class EOL(Token):
    required_annotations = set(["depth"])

    def annotate(self, scope: Scope, context: SemanticParseTree):
        i = 0
        for _ in scope.ancestors():
            i += 1
        self.annotations["depth"] = i

    def string(self):
        assert self.is_annotated()
        return "\n" + "\t" * self.annotations["depth"]
    
    def __str__(self):
        return "\\n"
