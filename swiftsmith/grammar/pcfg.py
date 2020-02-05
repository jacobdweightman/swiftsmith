from swiftsmith.grammar.cfg import Nonterminal, Production, CFG
from swiftsmith.grammar.parsetree import ParseTree

import random


class PProduction(Production):
    """
    Represents a production rule in a CFG, along with an associated probability.
    """
    def __init__(self, lhs, rhs, probability):
        super().__init__(lhs, rhs)
        self.probability = probability


class PCFG(CFG):
    ParseTree = ParseTree

    def __init__(self, start, productions):
        for rule in productions:
            assert isinstance(rule, PProduction), \
                "Attempted to create PCFG with non-probabilistic production. Use " \
                "PProduction instead."

        super().__init__(start, productions)
    
    def randomtree(self, start=None):
        """
        Take a random walk on a parse tree using the productions of the given grammar,
        using the specified symbol as its root.
        """
        if not start:
            start = self.start

        productions = {symbol: [] for symbol in self.nonterminals}
        weights = {symbol: [] for symbol in self.nonterminals}
        for rule in self:
            productions[rule.lhs].append(rule)
            weights[rule.lhs].append(rule.probability)

        tree = self.__class__.ParseTree(start)

        while tree.frontier:
            #print("\nFrontier: ", tree.frontier, "\n")
            subtree = random.choice(tree.frontier)
            symbol = subtree.value
            try:
                rule = random.choices(productions[symbol], weights=weights[symbol])[0]
            except IndexError:
                raise ValueError(f"Failed to expand symbol: {symbol}")
            #print("rule: ", rule)
            subtree.expand(rule.rhs)

        return tree
    
