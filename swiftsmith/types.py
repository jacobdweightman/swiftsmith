from collections import namedtuple
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
    ):
        self.access = access
        self.name = name
        self.instance_methods = instance_methods
        self.static_methods = static_methods
    
    def __eq__(self, other):
        return type(self) == type(other) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)


class EnumType(DataType):
    """
    Represents an enumeration datatype. This is a type whose values fit into one of a
    finite number of (enumerated) cases.
    """
    Case = namedtuple("EnumCase", ["name", "raw_value"])

    def __init__(self, name, access: AccessLevel=AccessLevel.internal):
        super().__init__(name, access=access)
        self.cases = {}
    
    def add_case(self, name, raw_value=None):
        """
        Adds a case with the given name to the enum.
        
        Note: this should only be called from inside the enum definition subtree.
        """
        self.cases[name] = EnumType.Case(name, raw_value)
    
    def choose_case_value(self):
        """Returns one of the cases of this enum as a string."""
        case = random.choice(list(self.cases.values()))
        # TODO: handle enums nested inside of other types
        return f"{self.name}.{case.name}"
    
    def case_with_raw_value(self, value):
        """Returns the case with the given raw value."""
        for case in self.cases.values():
            if case.raw_value == value:
                # TODO: handle enums nested inside of other types
                return f"{self.name}.{case.name}"

    def __str__(self):
        accessstr = str(self.access)
        if accessstr != "":
            accessstr += " "
        
        return f"{accessstr}enum {self.name}"
    
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
