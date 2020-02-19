from swiftsmith.grammar.parsetree import Tree, ParseTree
from swiftsmith.grammar.pcfg import PCFG

from collections import namedtuple
import random


class Scope(Tree):
    """
    Represents the symbols that are available in a lexical scope within a Swift program.
    """
    Variable = namedtuple("Variable", ["name", "datatype", "mutable"])
    Function = namedtuple("Function", ["name", "arguments", "returntype"])

    def __init__(self, parent=None):
        super().__init__(None, {})

        self.parent = parent
        self.variables = []
        self.functions = []
        self.deferred_stacks = []
        self.next_scope = self
    
    def declare(self, name, datatype, mutable):
        self.variables.append(Scope.Variable(name, datatype, mutable))
    
    def declare_func(self, name, arguments, returntype):
        self.functions.append(Scope.Function(name, arguments, returntype))
    
    def choose_variable(self, name=None, datatype=None, mutable=None):
        """
        Selects the name of a random variable that meets the given criteria.
        
        Note: throws an `IndexError` if no variables meet the criteria.
        """
        candidates = {var.name: var for var in self.variables}
        for scope in self.ancestors():
            for var in scope.variables:
                if var.name not in candidates: # narrower scopes shadow broader ones
                    candidates[var.name] = var
        
        candidates = list(candidates.values())

        if name is not None:
            candidates = filter(lambda n: n.name == name, candidates)
        if datatype is not None:
            candidates = filter(lambda n: n.datatype == datatype, candidates)
        if mutable is not None:
            candidates = filter(lambda n: n.mutable == mutable, candidates)
        
        candidates = list(candidates)
        return random.choice(candidates).name
    
    def choose_function(self, name=None, returntype=None):
        # TODO: traverse enclosing scopes as well
        candidates = self.functions

        if name:
            candidates = filter(lambda n: n.name == name, candidates)
        if returntype:
            candidates = filter(lambda n: n.returntype == returntype, candidates)
        
        return random.choice(candidates)
    
    def defer(self, closure):
        """
        Schedule some code to run when `pop_deferred` is called on this scope.
        """
        self.deferred_stacks[-1].append(closure)
    
    def push_deferred(self):
        self.deferred_stacks.append([])
    
    def pop_deferred(self):
        deferred = self.deferred_stacks.pop()

        while deferred:
            closure = deferred.pop()
            closure()

    def __contains__(self, key):
        if key in self.variables:
            return True
        elif not self.parent:
            return False
        else:
            return key in self.parent
