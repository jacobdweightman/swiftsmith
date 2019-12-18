from functools import reduce

from swiftsmith.grammar.cfg import Nonterminal

class LL1Parser(object):
    """
    Represents an LL(1) parser.

    An LL(1) parser is constructed from a context-free grammar. The LL(1) parsing
    algorithm first constructs a "parse table", and this parse table is then used to
    parse strings in the grammar (if the grammar is LL(1)) in linear time.

    LL(1) parsers can parse a strict subset of the grammars that LALR(1) or LR(1) can.
    There are some CFGs that are LL(1) but not LR(0), and some that are LR(0) but not
    LL(1).
    """
    
    def __init__(self, G):
        first = G.first_sets()
        follow = G.follow_sets()

        self.start = G.start
        self.table = {}

        for rule in G:
            if rule:
                for terminal in first[rule.rhs[0]]:
                    if (rule.lhs, terminal) not in self.table:
                        self.table[rule.lhs, terminal] = rule.rhs
                    else:
                        raise ValueError("Attempted to create LL(1) parser for "
                                        "non-LL(1) grammar.")

            if all(["" in first[n] for n in rule.rhs]):
                for terminal in follow[rule.lhs]:
                    if (rule.lhs, terminal) not in self.table:
                        self.table[rule.lhs, terminal] = rule.rhs
                    else:
                        raise ValueError("Attempted to create LL(1) parser for "
                                         "non-LL(1) grammar.")
    
    def parse(self, tokens):
        tokens = (*tokens, "\0")
        stack = ["\0", self.start]
        index = 0

        while stack:
            symbol = stack.pop()
            if isinstance(symbol, Nonterminal):
                try:
                    stack.extend(self.table[symbol, tokens[index]][::-1])
                except KeyError:
                    return False
            else:
                if symbol == tokens[index]:
                    index += 1
                else:
                    return False
        
        return True
