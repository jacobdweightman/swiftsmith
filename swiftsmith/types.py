from collections import namedtuple
import copy
import random
from enum import Enum, IntEnum, auto

class AccessLevel(IntEnum):
    """Represents the possible access control levels."""
    private = 0
    fileprivate = 1 # This is equivalent to internal in a single-file module.
    internal = 1
    public = 2
    open = 2

    def __str__(self):
        if self == AccessLevel.private:
            return "private"
        elif self == AccessLevel.fileprivate:
            return "fileprivate"
        elif self == AccessLevel.internal:
            return ""
        elif self == AccessLevel.public:
            return "public"
        elif self == AccessLevel.open:
            return "open"
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
            genstr = "<" + ", ".join([t.name for t in self.generic_types.values()]) + ">"
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
        arguments: dict,
        returntype: DataType,
        syntax: CallSyntax=CallSyntax.normal,
        generic_types=[],
    ):
        argstring = ", ".join([f"{n}: {t}" for n,t in arguments.items()])
        super().__init__(name=f"({argstring}) -> {returntype}", generic_types=generic_types)
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
