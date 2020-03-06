from collections import namedtuple
import random
from enum import IntEnum

class AccessLevel(IntEnum):
    private = 0
    fileprivate = 1 # This is equivalent to internal in a single-file module.
    internal = 1
    public = 2
    open = 2

class DataType(object):
    """The parent class of all Swift datatypes."""
    def __init__(self, name: str, access: AccessLevel=AccessLevel.internal):
        self.access = access
        self.name = name

    def __str__(self):
        return self.name
    
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

    def __init__(self, name, access: AccessLevel=AccessLevel.internal, raw_type=type(None)):
        assert raw_type in {type(None), Int}
        super().__init__(name, access=access)
        self.raw_type = raw_type
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


class Struct(DataType):
    """
    Represents a struct type in Swift.

    For more information on the differences between structs and classes in Swift, see
    https://docs.swift.org/swift-book/LanguageGuide/ClassesAndStructures.html
    """
    pass

########################################
#   Standard Library Types             #
########################################

Int = Struct("Int")
Bool = Struct("Bool")
