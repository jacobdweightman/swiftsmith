from .grammar import Nonterminal, PProduction
from .scope import Scope
from .formatting import EOL, block
from .semantics import Token, PCFG
from .names import identifier

import random

########################################
#   Tokens                             #
########################################

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

########################################
#   Nonterminals                       #
########################################

funcdeclaration = Nonterminal("FUNC_DECLARATION")

########################################
#   Grammar                            #
########################################

function_grammar = PCFG(
    funcdeclaration,
    [
        PProduction(funcdeclaration, (EOL(), EOL(), "func ", Function(), " {", block, EOL(), "}"), 1.0),
    ]
)
