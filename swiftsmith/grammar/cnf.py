import swiftsmith.grammar.cfg as cfg

from functools import reduce

class CNF(cfg.CFG):
    """
    Represents a context-free grammar that is in Chomsky normal form (CNF).

    A grammar is in CNF if:
     * All of its productions are of the form A -> BC, A -> 'a', or S -> ''
     * The start symbol does not occur on the right side of a production
    """

    def __init__(self, grammar):
        pass

    @classmethod
    def eliminate_start_from_rhs(cls, grammar):
        """
        Given a CFG, produces an equivalent grammar where the start symbol does not
        occur on the right side of any productions. If there are no such productions,
        the grammar is returned unchanged. If there is, then a new start symbol S' is
        introduced with the production S' -> S.
        """
        add_new_start = False
        for rule in grammar:
            if grammar.start in rule.rhs:
                add_new_start = True
                break
        
        if add_new_start:
            start = grammar.cfg.Nonterminal("S'")
            return grammar.cfg.CFG(
                start,
                grammar.productions + grammar.cfg.Production(start, grammar.start)
            )
        else:
            return grammar