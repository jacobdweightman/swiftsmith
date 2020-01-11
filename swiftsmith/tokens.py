from .grammar.cfg import Nonterminal
from .names import identifier
from .scope import Scope

import random


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


class Variable(Token):
    """
    Represents a Swift variable.
    """
    def __init__(self, datatype=None, declaration=False, mutable=False):
        self.datatype = datatype
        self.declaration = declaration
        self.mutable = mutable

    def string(self, scope):
        if self.declaration:
            name = next(identifier)

            # This name isn't usable in a declaration with an initial value. We defer
            # adding this variable to the scope until after it is declared.
            closure = (lambda: scope.declare(name, "Int", self.mutable))
            scope.defer(closure)

            return name
        else:
            if scope.variables:
                return scope.choose_variable()
            else:
                # if there are no variables of the correct type in scope, fall back to a
                # literal value.
                if self.datatype == "Int":
                    return Int().string(scope)
                elif self.datatype == "Bool":
                    return Bool().string(scope)
                else:
                    raise ValueError(f"Cannot construct literal of type `{self.datatype}`")


class Int(Token):
    def string(self, scope):
        return str(random.randint(0, 5))


class Bool(Token):
    def string(self, scope):
        return random.choice(["true", "false"])


class Function(Token):
    def string(self, scope: Scope):
        # TODO: Declare function
        name = next(identifier)

        arguments = {}
        for _ in range(random.randint(0, 3)):
            arguments[next(identifier)] = "Int"

        returntype = "Int"
        scope.declare_func(name, arguments, returntype)
        argstring = ', '.join(k + ": " + v for (k,v) in arguments.items())

        return name + "(" + argstring + ") -> Int"


class Block(Token):
    def __init__(self, returntype=None):
        self.returntype = returntype
    
    def string(self, scope):
        # "push" a new scope nested in the current one
        scope.next_scope = Scope(parent=scope)

        def closure():
            # "pop" the scope once its content has been generated
            scope.next_scope = scope
        scope.defer(closure)

        return ""


class EOL(Token):
    def string(self, scope):
        i = 0
        for _ in scope.ancestors():
            i += 1
        return "\n" + "\t" * i
