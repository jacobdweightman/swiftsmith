from .grammar import Nonterminal, PProduction
from .branch import branch_grammar
from .enum import enum_grammar, enum
from .function import function_grammar, FuncDeclaration
from .statement import statement_grammar, DeclarationAssignment
from .formatting import EOL
from .semantics import SemanticPCFG

S = Nonterminal("S")

swift = SemanticPCFG(
    S,
    [
        # Allow variable declarations and functions at the top level of a program.
        PProduction(S, (DeclarationAssignment(None), S), 0.2),
        PProduction(S, (FuncDeclaration(), S), 0.2),
        PProduction(S, (enum, S), 0.2),
        PProduction(S, (FuncDeclaration(),), 0.4), # Guarantee at least one function
    ]
) + branch_grammar \
  + function_grammar \
  + statement_grammar \
  + enum_grammar
