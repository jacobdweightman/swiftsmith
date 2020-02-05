from .grammar import Nonterminal, PProduction
from .scope import Scope
from .branch import branch_statement
from .expression import expression
from .formatting import EOL, Block
from .statement import assignment
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
block = Nonterminal("FUNC_BLOCK")
statements = Nonterminal("FUNC_STATEMENTS")
statement = Nonterminal("FUNC_STATEMENT")

########################################
#   Grammar                            #
########################################

function_grammar = PCFG(
    funcdeclaration,
    [
        PProduction(funcdeclaration, (EOL(), EOL(), "func ", Function(), " {", block, EOL(), "}"), 1.0),
        PProduction(block, (Block(), statements), 1.0),

        PProduction(statements, (statement, statements), 0.7),
        PProduction(statements, (EOL(), "return ", expression("Int")), 0.3),
        PProduction(statement, (assignment,), 0.7),
        PProduction(statement, (branch_statement,), 0.3)
    ]
)
