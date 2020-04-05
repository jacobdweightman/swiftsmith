from .scope import Scope
from .semantics import SemanticParseTree, Token
from .types import AccessLevel

########################################
#   Tokens                             #
########################################

class AccessModifier(Token):
    """Represents an access modifier as would appear in a symbol declaration."""
    required_annotations = {"access"}

    def __init__(self, at_least: AccessLevel=AccessLevel.private, at_most: AccessLevel=None):
        super().__init__()
        self.at_least = at_least
        self.at_most = at_most
    
    def annotate(self, scope: Scope, context: SemanticParseTree):
        parent = context.parent.value
        if parent.annotations["locked"]:
            self.annotations["access"] = parent.annotations["access"]
        else:
            level = AccessLevel.random(at_least=self.at_least, at_most=self.at_most)
            context.parent.value.annotations["access"] = level
            self.annotations["access"] = level
    
    def string(self):
        assert self.is_annotated()
        accessstr = str(self.annotations["access"])
        if accessstr != "":
            accessstr += " "
        return accessstr 
