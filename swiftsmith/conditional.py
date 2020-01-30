from .expression import expression
from .formatting import EOL, block
from .grammar import Nonterminal, PProduction
from .semantics import Token, SemanticPCFG

########################################
#   Nonterminals                       #
########################################

ifstatement = Nonterminal("IF_STATEMENT")
conditionlist = Nonterminal("CONDITION_LIST")
condition = Nonterminal("CONDITION")

########################################
#   Grammar                            #
########################################

conditional_grammar = SemanticPCFG(
    ifstatement,
    [
        PProduction(ifstatement, (EOL(), "if ", conditionlist, " {", block, EOL(), "}"), 0.5),
        PProduction(ifstatement, (EOL(), "if ", conditionlist, " {", block, EOL(), "} else {", block, EOL(), "}"), 0.5),
        PProduction(conditionlist, (condition,), 1.0),
        PProduction(conditionlist, (condition, ", ", conditionlist), 0.2),
        PProduction(condition, (expression("Bool"),), 1.0),
    ]
)
