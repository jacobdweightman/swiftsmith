from .grammar import Nonterminal, PProduction, PCFG
from .branch import branch_grammar
from .expression import expression_grammar
from .function import function_grammar, funcdeclaration
from .statement import statement_grammar, assignment
from .formatting import EOL
from .semantics import SemanticPCFG

S = Nonterminal("S")

swift = SemanticPCFG(
    S,
    [
        # Allow variable declarations and functions at the top level of a program.
        PProduction(S, (assignment, S), 0.3),
        PProduction(S, (funcdeclaration, S), 0.3),
        PProduction(S, (funcdeclaration,), 0.4), # Guarantee at least one function
    ]
) + branch_grammar \
  + expression_grammar \
  + function_grammar \
  + statement_grammar
