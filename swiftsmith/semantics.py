from .grammar import ParseTree, PCFG
from .scope import Scope

class Token(object):
    """
    The base class of all types of tokens in a grammar.
    
    If a subclass of Token is used as a terminal in a production, then that type's
    constructor is called when a symbol in a parse tree is expanded using that
    production. The string method is called when converting the parse tree to the text
    of a program.
    """
    def string(self, scope):
        raise NotImplementedError()


class SemanticParseTree(ParseTree):
    def string(self, scope=Scope()):
        """
        Get the string of terminals represented by this parse tree.
        """
        if self.isleaf():
            if isinstance(self.value, Token):
                return self.value.string(scope)
            return str(self.value)
        
        scope.push_deferred()
        children = [child.string(scope=scope.next_scope) for child in self.children]
        scope.pop_deferred()
        return "".join(children)


class SemanticPCFG(PCFG):
    """
    Represents a probabalistic context free grammar where parse trees have attached
    semantic information, in order to constrain the allowable strings.
    """
    ParseTree = SemanticParseTree
