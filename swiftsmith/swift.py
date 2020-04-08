from .grammar import Nonterminal, PProduction
from .branch import branch_grammar
from .enum import enum_grammar, EnumDeclaration
from .function import function_grammar, FuncDeclaration
from .statement import statement_grammar, DeclarationAssignment
from .formatting import EOL
from .semantics import SemanticPCFG
from .types import AccessLevel

S = Nonterminal("S")

swift = SemanticPCFG(
    S,
    [
        # Allow variable declarations and functions at the top level of a program.
        #PProduction(S, (DeclarationAssignment(None), S), 0.2),
        PProduction(S, (FuncDeclaration(), S), 0.4),
        PProduction(S, (EnumDeclaration(), S), 0.2),
        # Guarantee at least one public function
        PProduction(S, (FuncDeclaration(access=AccessLevel.public),), 0.2),
    ]
) + branch_grammar \
  + function_grammar \
  + statement_grammar \
  + enum_grammar
