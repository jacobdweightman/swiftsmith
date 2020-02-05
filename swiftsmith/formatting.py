from .grammar import Nonterminal
from .scope import Scope
from .semantics import Token

########################################
#   Tokens                             #
########################################

class Block(Token):
    def __init__(self, returntype=None):
        self.returntype = returntype
    
    def string(self, scope):
        # "push" a new scope nested in the current one
        scope.next_scope = Scope(parent=scope)

        def closure():
            # "pop" the scope once its content has been generated
            scope.next_scope = scope
        scope.defer(closure)

        return ""
    
    def __str__(self):
        return f"Block({self.returntype or ''})"


class EOL(Token):
    def string(self, scope):
        i = 0
        for _ in scope.ancestors():
            i += 1
        return "\n" + "\t" * i
    
    def __str__(self):
        return "\\n"
