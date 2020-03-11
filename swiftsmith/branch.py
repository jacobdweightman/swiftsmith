from .expression import Expression
from .formatting import Block, EOL
from .grammar import Nonterminal, PProduction
from .statement import Assignment
from .semantics import Token, SemanticPCFG
from .types import Bool

########################################
#   Nonterminals                       #
########################################

branch_statement = Nonterminal("BRANCH_STATEMENT")
if_statement = Nonterminal("IF_STATEMENT")
else_clause = Nonterminal("ELSE_CLAUSE")
conditionlist = Nonterminal("CONDITION_LIST")
condition = Nonterminal("CONDITION")
block = Nonterminal("BRANCH_BLOCK")
statements = Nonterminal("BRANCH_BLOCK_STATEMENTS")
statement = Nonterminal("BRANCH_BLOCK_STATEMENT")
# TODO: prefix nonterminals when combining grammars

########################################
#   Grammar                            #
########################################

branch_grammar = SemanticPCFG(
    branch_statement,
    [
        # TODO: support guard and switch statements
        PProduction(branch_statement, (if_statement,), 1.0),

        PProduction(if_statement, (EOL(), "if ", conditionlist, " {", block, EOL(), "}"), 0.5),
        PProduction(if_statement, (EOL(), "if ", conditionlist, " {", block, EOL(), "}", else_clause), 0.5),
        PProduction(else_clause, (" else {", block, EOL(), "}"), 1.0),

        PProduction(conditionlist, (condition,), 0.8),
        PProduction(conditionlist, (condition, ", ", conditionlist), 0.2),
        PProduction(condition, (Expression(Bool),), 1.0),

        PProduction(block, (Block(), statements), 1.0),
        PProduction(statements, (statement, statements), 0.6),
        PProduction(statements, (statement,), 0.4), # guarantee at least one statement

        PProduction(statement, (Assignment(None),), 0.8),
        PProduction(statement, (branch_statement,), 0.2), # be warry of recursion
    ]
)
