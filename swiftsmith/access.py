from .scope import Scope
from .semantics import SemanticParseTree, Token
from .types import AccessLevel

########################################
#   Tokens                             #
########################################

class AccessModifier(Token):
    """Represents an access modifier as would appear in a symbol declaration."""
    required_annotations = {"access"}

    def __init__(self, at_most=None):
        super().__init__()
        self.at_most = at_most
    
    def annotate(self, scope: Scope, context: SemanticParseTree):
        level = AccessLevel.random(at_most=self.at_most)
        context.parent.value.annotations["access"] = level
        self.annotations["access"] = level
    
    def string(self):
        assert self.is_annotated()
        accessstr = str(self.annotations["access"])
        if accessstr != "":
            accessstr += " "
        return accessstr 
