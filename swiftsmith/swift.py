from .grammar import Nonterminal, PProduction, PCFG
from .expression import expression_grammar, expression, Variable
from .conditional import conditional_grammar, ifstatement
from .formatting import Block, EOL, block
from .function import function_grammar, funcdeclaration
from .semantics import SemanticPCFG

S = Nonterminal("S")
statement = Nonterminal("STATEMENT")
declaration = Nonterminal("DECLARATION")
returnstatement = Nonterminal("RETURN")

swift = SemanticPCFG(
    S,
    [
        # Allow variable declarations and functions at the top level of a program.
        PProduction(S, (declaration, S), 0.3),
        PProduction(S, (funcdeclaration, S), 0.3),
        PProduction(S, (funcdeclaration,), 0.4), # Guarantee at least one function

        PProduction(statement, (declaration,), 0.8),
        PProduction(statement, (ifstatement,), 0.2),
        PProduction(statement, (returnstatement,), 0.),

        PProduction(declaration, (EOL(), "let ", Variable(declaration=True), " = ", expression("Int")), 0.3),
        PProduction(declaration, (EOL(), "var ", Variable(declaration=True, mutable=True), " = ", expression("Int")), 0.7),

        PProduction(returnstatement, (EOL(), "return ", expression("Int")), 1.0),

        PProduction(block, (Block(), statement, statement, returnstatement), 1.0),
    ]
) + expression_grammar \
  + conditional_grammar \
  + function_grammar
