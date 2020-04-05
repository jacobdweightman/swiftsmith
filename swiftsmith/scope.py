from swiftsmith.grammar.parsetree import Tree, ParseTree
from swiftsmith.grammar.pcfg import PCFG
from swiftsmith.types import AccessLevel, CallSyntax, DataType, FunctionType
from swiftsmith.standard_library import Bool, Int, Optional

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
        self.functions = {}
        self.next_scope = self

    def import_standard_library(self):
        """
        Adds standard library types to the given scope.
        
        Note that these types will be accessible from all scopes enclosed by the given
        as well.
        """
        self.add_child(Scope(datatype=Bool))
        self.add_child(Scope(datatype=Int))
        self.add_child(Scope(datatype=Optional))

    def declare(self, name, datatype, mutable):
        self.variables.append(Scope.Variable(name, datatype, mutable))
    
    def declare_func(self, access, name, arguments, returntype):
        self.functions[name] = FunctionType(access, arguments, returntype)
    
    def accessible_variables(self, name: str=None, datatype: DataType=None, mutable: bool=None):
        """
        Returns the set of variables that are accessible in this lexical scope and
        match the given criteria.
        """
        variables = {var.name: var for var in self.variables}
        for scope in self.ancestors():
            for var in scope.variables:
                if var.name not in variables: # narrower scopes shadow broader ones
                    variables[var.name] = var
        
        variables = variables.values()
        if name is not None:
            variables = filter(lambda n: n.name == name, variables)
        if datatype is not None:
            variables = filter(lambda n: n.datatype == datatype, variables)
        if mutable is not None:
            variables = filter(lambda n: n.mutable == mutable, variables)

        return list(variables)

    def choose_variable(self, name: str=None, datatype: DataType=None, mutable: bool=None):
        """
        Selects the name of a random variable that meets the given criteria.
        
        Note: throws an `IndexError` if no variables meet the criteria.
        """
        candidates = list(self.accessible_variables(name=name, datatype=datatype, mutable=mutable))
        return random.choice(candidates)
    
    def accessible_functions(self, name=None, returntype=None, at_least: AccessLevel=None):
        """
        Returns a dictionary of functions that are accessible in this lexical scope.
        
        The keys of this dictionary are function names, and the values are function
        types. This dictionary includes functions that are not bound to a type as well
        as static methods of accessible types.
        """
        functions = {name: f for name, f in self.functions.items()}
        for scope in self.ancestors():
            for name, f in scope.functions.items():
                if name not in functions: # narrower scopes shadow broader ones
                    functions[name] = f

        for _type in self.accessible_types():
            for methodname, ftype in _type.static_methods.items():
                if ftype.syntax == CallSyntax.normal:
                    methodname = f"{_type.name}.{methodname}"
                functions[methodname] = ftype
        
        if name is not None:
            functions = dict(filter(lambda e: e[0] == name, functions.items()))
        if returntype is not None:
            functions = dict(filter(lambda e: e[1].returntype == returntype, functions.items()))
        if at_least is not None:
            functions = dict(filter(lambda e: e[1].access >= at_least, functions.items()))
        
        return functions

    def choose_function(self, name=None, returntype=None, at_least: AccessLevel=None):
        candidates = self.accessible_functions(name=name, returntype=returntype, at_least=at_least)
        return random.choice(list(candidates.items()))
    
    def accessible_types(self):
        """Returns a list of all types that are accessible in this lexical scope."""
        types = []
        # all nested types are accessible
        for nestedtype in self.preorder():
            # Note: nestedtype is either a DataType object or None.
            if isinstance(nestedtype, DataType):
                types.append(nestedtype)
        
        # all enclosing types are accessible
        for enclosingscope in self.ancestors():
            # including ancestors and their siblings
            for siblingscope in enclosingscope.children:
                if isinstance(siblingscope.value, DataType) and siblingscope is not self:
                    types.append(siblingscope.value)
            
            if isinstance(enclosingscope.value, DataType):
                types.append(enclosingscope.value)
        
        # removing self prevents declaration of recursive types
        return [t for t in types if t is not self.value]
    
    def choose_type(self):
        """Returns a random Swift type that is available in this lexical scope."""
        candidates = self.accessible_types()
        return random.choice(candidates)
    
    def specialize_type(self, datatype: DataType):
        """Specializes a generic type using types accessible from this scope."""
        unspecialized = {k for k,v in datatype.generic_types.items() if v is None}
        types = list(filter(lambda t: len(t.generic_types) == 0, self.accessible_types()))
        
        specializations = {}
        for t in unspecialized:
            specializations[t.name] = random.choice(types)
        
        return datatype.specialize(**specializations)

