from .grammar import Nonterminal, PProduction
from .scope import Scope
from .branch import branch_statement
from .expression import Expression
from .formatting import EOL, Block
from .statement import Assignment
from .semantics import Token, PCFG, SemanticParseTree, SemanticNonterminal
from .names import identifier
from .types import Int

import random

########################################
#   Tokens                             #
########################################

class Function(Token):
    required_annotations = set(["name", "arguments", "returntype"])

    def annotate(self, scope: Scope, context: SemanticParseTree):
        self.annotations["name"] = next(identifier)

        arguments = {}
        for _ in range(random.randint(1, 3)):
            arguments[next(identifier)] = Int
        self.annotations["arguments"] = arguments

        # TODO: allow non-Int return types
        self.annotations["returntype"] = Int

        scope.declare_func(
            self.annotations["name"],
            self.annotations["arguments"],
            self.annotations["returntype"]
        )

        def closure():
            for argument, datatype in arguments.items():
                scope.children[-1].declare(argument, datatype, False)
        context.parent.childwhere(lambda n: n.value == block).children[0].defer(closure)
    
    def string(self):
        assert self.is_annotated()
        name = self.annotations["name"]
        arguments = self.annotations["arguments"]
        returntype = self.annotations["returntype"]

        argstring = ', '.join(k + ": " + v.name for (k,v) in arguments.items())
        
        return f"{name}({argstring}) -> {returntype.name}"

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
        PProduction(statements, (EOL(), "return ", Expression(Int)), 0.3),
        PProduction(statement, (Assignment(None),), 0.7),
        PProduction(statement, (branch_statement,), 0.3)
    ]
)
