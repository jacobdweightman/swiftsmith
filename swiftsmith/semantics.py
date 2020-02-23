from collections import deque

from .grammar import ParseTree, PCFG, Nonterminal
from .scope import Scope

class Annotatable(object):
    """
    Represents a value which may have annotations as would appear in a semantic parse
    tree.
    """
    required_annotations: set = set([])

    def __init__(self, *args, **kwargs):
        self.annotations = {}
    
    def is_annotated(self) -> bool:
        return self.__class__.required_annotations.issubset(self.annotations)
    
    def annotate(self, scope: Scope, context):
        raise NotImplementedError(f"'{self.__class__}' does not implement 'annotate(scope)'")

    def string(self):
        raise NotImplementedError(f"'{self.__class__}' does not implement 'string()'")


class SemanticNonterminal(Nonterminal, Annotatable):
    """
    Represents a nonterminal symbol in a grammar which may have additional context-
    dependent information attached through annotations.
    """
    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, cls.__name__)
    
    def __init__(self, *args, **kwargs):
        Annotatable.__init__(self, *args, **kwargs)


class Token(Annotatable):
    """
    Represents a "terminal" string in a context free grammar, but whose exact string
    value depends on its context.
    
    If a subclass of Token is used as a terminal in a production, then that type's
    constructor is called when a symbol in a parse tree is expanded using that
    production. The `annotate` method will be called by the `annotate` method of the
    `SemanticParseTree`. The string value of the token is then given by the `string`
    method, which is called by the `string` method of the `SemanticParseTree`.
    """
    pass


class SemanticParseTree(ParseTree):
    """
    Represents a parse tree with additional semantic (context-dependent) information.
    
    Changes in traversal state may also be deferred until later using the `defer`
    method. Deferred methods are run immediately after the tree has been annotated.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._deferred_actions = deque()
    
    def annotate(self, scope=Scope()):
        """
        Add annotations with semantic information to nodes of this tree.
        
        Performs a preorder, depth-first traversal of the tree, annotating nodes with
        any required semantic (context-dependent) information from their neighbors.
        """
        # TODO: check only for strings once `Nonterminals` are `Annotatable`.
        if isinstance(self.value, Annotatable):
            self.value.annotate(scope.next_scope, self)
        
        if self.children is not None:
            for child in self.children:
                child.annotate(scope=scope.next_scope)
        
        self._run_deferred()
    
    def string(self):
        """Get the string of terminals represented by this parse tree."""
        if self.isleaf():
            if isinstance(self.value, Token):
                return self.value.string()
            return str(self.value)
        
        children = [child.string() for child in self.children]
        return "".join(children)
    
    def defer(self, closure):
        """
        Defers execution of the given closure until `run_deferred` is called.

        Note: closure must be callable and take no arguments.
        """
        self._deferred_actions.append(closure)
    
    def _run_deferred(self):
        """
        Runs all deferred actions on this nonterminal in the order they were added.
        """
        while self._deferred_actions:
            action = self._deferred_actions.popleft()
            action()


class SemanticPCFG(PCFG):
    """
    Represents a probabalistic context free grammar where parse trees have attached
    semantic information, in order to constrain the allowable strings.
    """
    ParseTree = SemanticParseTree
