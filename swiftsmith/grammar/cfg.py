from functools import lru_cache

class Nonterminal(str):
    """
    Represents a nonterminal in sentential forms of a CFG.
    
    They behave like a string in every way, but may be distinguished from terminal
    symbols in a grammar using `isinstance(a, Nonterminal)`.
    """
    pass


class Production(object):
    """
    Represents a production rule of a CFG.

    A production represents a rewriting rule, whereby the nonterminal on the left side
    of a sentential form may be replaced by the sequence of nonterminals and terminals
    on the right side in a derivation.
    """

    def __init__(self, lhs, rhs):
        assert isinstance(lhs, Nonterminal), "CFG production must have Nonterminal LHS"
        self.lhs = lhs
        self.rhs = tuple(rhs)
    
    def __str__(self):
        return str(self.lhs) + " \u2192 " + "".join(map(str, self.rhs))
    
    def __bool__(self):
        return bool(self.rhs)
    
    def __hash__(self):
        return hash((self.lhs, self.rhs))

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs


class CFG(tuple):
    """
    Represents a context free grammar (CFG).

    A CFG consists of a set of nonterminal symbols, a set of terminal symbols, a
    designated start symbol (which is itself a nonterminal), and a set of "productions"
    for rewriting nonterminals. In this implementation, only the start symbol and
    productions must be specified; the nonterminals and terminals are inferred.

    The language of a CFG is the set of strings that may be derived from the start
    symbol by rewriting any nonterminals with the right side of any production.

    Example:
    Consider the grammar with start symbol S
    S -> (S, "a")
    S -> ("a",)

    Some derivations of strings in this grammar are:
    S => a                  so "a" is in the language of the grammar
    S => Sa => aa           so "aa" is in the language of the grammar
    S => Sa => Saa => aaa   so "aaa" is in the language of the grammar
    ...
    """

    def __new__(cls, start, productions):
        return super().__new__(cls, tuple(productions))

    def __init__(self, start, productions):
        assert isinstance(start, Nonterminal), "CFG start symbol must be a Nonterminal"
        self.start = start

        self.nonterminals = set()
        self.terminals = set()

        for production in self:
            self.nonterminals.add(production.lhs)
            for symbol in production.rhs:
                if isinstance(symbol, Nonterminal):
                    self.nonterminals.add(symbol)
                else:
                    self.terminals.add(symbol)

    def __add__(self, other):
        """
        Produces a new grammar with the left addend's start symbol and the union of the
        addends' productions.
        """
        return type(self)(self.start, super().__add__(other))

    def _empty_productions(self):
        """
        Returns the productions of the grammar that produce the empty string.
        """
        return filter(bool, self)

    def __str__(self):
        return "CFG:\n\t" + "\n\t".join(map(str, self))

    def __hash__(self):
        return hash((self.start, super().__hash__()))
