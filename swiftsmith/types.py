from collections import namedtuple
import copy
import random
from enum import Enum, IntEnum, auto

class AccessLevel(IntEnum):
    """Represents the possible access control levels."""
    # Hidden to all other scopes (e.g. symbol declared inside a function)
    local = 0

    # Accessible only to child scopes.
    private = 1

    # Accessible to any scope in the same file.
    fileprivate = 2

    # Accessible to any scope in the same module.
    internal = 3

    # Accessible to any scope in the same module or an importing module.
    public = 4

    @classmethod
    def random(cls, at_least=1, at_most=None):
        """
        Picks a random access level.

        If at_least is specified, the chosen access level will be at least as broad as
        the given access level.

        If at_most is specified, the chosen access level will be at most as broad as
        the given access level.
        """
        candidates = zip(list(cls), [0.0, 0.3, 0.1, 0.2, 0.4])

        if at_least is not None:
            candidates = filter(lambda a: a[0] >= at_least, candidates)
        if at_most is not None:
            candidates = filter(lambda a: a[0] <= at_most, candidates)

        candidates, weights = zip(*candidates)
        return random.choices(candidates, weights=weights)[0]

    def __str__(self):
        if self == AccessLevel.private:
            return "private"
        elif self == AccessLevel.fileprivate:
            return "fileprivate"
        elif self == AccessLevel.internal:
            return ""
        elif self == AccessLevel.public:
            return "public"
        raise NotImplementedError()


class CallSyntax(Enum):
    """Represents the possible function call syntaxes."""
    normal = auto()
    prefix = auto()
    infix = auto()
    postfix = auto()


class DataType(object):
    """The parent class of all Swift datatypes."""
    def __init__(
        self,
        name: str,
        access: AccessLevel=AccessLevel.internal,
        instance_methods = {},
        static_methods = {},
        generic_types={},
        newvaluefactory=None,
    ):
        self.access = access
        self.name = name
        self.instance_methods = instance_methods
        self.static_methods = static_methods
        self.generic_types = generic_types
        self._newvaluefactory = newvaluefactory
    
    def newvalue(self):
        """Returns an expression for a new value of this type."""
        if self._newvaluefactory is not None:
            return self._newvaluefactory()
        raise NotImplementedError()
    
    def specialize(self, **kwargs):
        """Creates a copy of this type with the given generics specialized."""
        datatype = copy.deepcopy(self)
        generics = {t.name: t for t in self.generic_types.keys()}
        for gtname, ct in kwargs.items():
            gt = generics[gtname]
            datatype.generic_types[gt] = ct
        return datatype
    
    def is_fully_specialized(self):
        """Checks that all of this type's generics have been specialized."""
        return None not in self.generic_types.values()
    
    def full_name(self):
        """Returns the full name of the type, including generics."""
        if len(self.generic_types) > 0:
            gts = [ct if ct is not None else gt for gt,ct in self.generic_types.items()]
            genstr = "<" + ", ".join([t.full_name() for t in gts]) + ">"
        else:
            genstr = ""
        return self.name + genstr

    def __eq__(self, other):
        return type(self) == type(other) and self.name == other.name \
               and self.generic_types == other.generic_types
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        accessstr = str(self.access)
        if accessstr != "":
            accessstr += " "
        
        return f"{accessstr}datatype {self.name}"
    
    def __repr__(self):
        return str(self)


class EnumType(DataType):
    """
    Represents an enumeration datatype. This is a type whose values fit into one of a
    finite number of (enumerated) cases.
    """
    Case = namedtuple("EnumCase", ["name", "associatedvalues"])

    def __init__(self, name, access: AccessLevel=AccessLevel.internal, generic_types={}):
        super().__init__(name, access=access, generic_types=generic_types)
        self.cases = {}
    
    def add_case(self, name, associatedvalues):
        """
        Adds a case with the given name to the enum.
        
        Note: this should only be called from inside the enum definition subtree.
        """
        self.cases[name] = EnumType.Case(name, associatedvalues)
    
    def newvalue(self):
        """Returns one of the cases of this enum as a string."""
        assert self.is_fully_specialized()
        case = random.choice(list(self.cases.values()))

        associatedvaluetypes = [t for t in case.associatedvalues]
        for i, avt in enumerate(associatedvaluetypes):
            if avt in self.generic_types:
                associatedvaluetypes[i] = self.generic_types[avt]
        
        associatedvalues = [av.newvalue() for av in associatedvaluetypes]
        if len(associatedvalues) > 0:
            avstr = "(" + ", ".join(associatedvalues) + ")"
        else:
            avstr = ""
        
        # TODO: handle enums nested inside of other types
        return f"{self.full_name()}.{case.name}{avstr}"

    def __str__(self):
        accessstr = str(self.access)
        if accessstr != "":
            accessstr += " "
        
        return f"{accessstr}enum {self.name}"
    
    def __repr__(self):
        return str(self)


class FunctionType(DataType):
    def __init__(
        self,
        access: AccessLevel,
        arguments: dict,
        returntype: DataType,
        syntax: CallSyntax=CallSyntax.normal,
        generic_types={},
    ):
        argstring = ", ".join([f"{n}: {t.full_name()}" for n,t in arguments.items()])
        super().__init__(name=f"({argstring}) -> {returntype.full_name()}", access=access, generic_types=generic_types)
        self.arguments = arguments
        self.returntype = returntype

        if syntax == CallSyntax.prefix:
            assert len(arguments) == 1, f"expected 1 argument for prefix operator, got {len(arguments)}"
        if syntax == CallSyntax.infix:
            assert len(arguments) == 2, f"expected 2 arguments for infix operator, got {len(arguments)}"
        if syntax == CallSyntax.postfix:
            assert len(arguments) == 1, f"expected 1 argument for postfix operator, got {len(arguments)}"

        self.syntax = syntax
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)


class Struct(DataType):
    """
    Represents a struct type in Swift.

    For more information on the differences between structs and classes in Swift, see
    https://docs.swift.org/swift-book/LanguageGuide/ClassesAndStructures.html
    """
    def __str__(self):
        accessstr = str(self.access)
        if accessstr != "":
            accessstr += " "
        
        return f"{accessstr}struct {self.name}"
    
    def __repr__(self):
        return str(self)
