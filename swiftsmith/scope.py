from swiftsmith.grammar.parsetree import Tree, ParseTree
from swiftsmith.grammar.pcfg import PCFG
from swiftsmith.types import DataType
from swiftsmith.standard_library import Bool, Int

from collections import namedtuple
import random


class Scope(Tree):
    """
    Represents the symbols that are available in a lexical scope within a Swift program.

    A scope is tree whose value is a datatype if the scope represents a type, or None if
    it doesn't. For example, the value of the lexical scope of a struct will be that
    struct, but the value of the lexical scope of an if statement will be None. 
    """
    Variable = namedtuple("Variable", ["name", "datatype", "mutable"])
    Function = namedtuple("Function", ["name", "arguments", "returntype"])

    def __init__(self, parent=None, datatype=None):
        super().__init__(datatype, {})

        self.parent = parent
        self.variables = []
        self.functions = []
        self.next_scope = self

    def import_standard_library(self):
        """
        Adds standard library types to the given scope.
        
        Note that these types will be accessible from all scopes enclosed by the given
        as well.
        """
        self.add_child(Scope(datatype=Bool))
        self.add_child(Scope(datatype=Int))

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
    
    def choose_type(self):
        """Returns a random Swift type that is available in this lexical scope."""
        candidates = []
        # all nested types are accessible
        for nestedtype in self.preorder():
            # Note: nestedtype is either a DataType object or None.
            if isinstance(nestedtype, DataType):
                candidates.append(nestedtype)
        
        # all enclosing types are accessible
        for enclosingscope in self.ancestors():
            # including ancestors and their siblings
            for siblingscope in enclosingscope.children:
                if isinstance(siblingscope.value, DataType):
                    candidates.append(siblingscope.value)
            
            if isinstance(enclosingscope.value, DataType):
                candidates.append(enclosingscope.value)
        
        return random.choice(candidates)
