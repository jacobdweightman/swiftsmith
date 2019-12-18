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

    @lru_cache(maxsize=1)
    def first_sets(self):
        """
        For each symbol in the grammar, computes the set of terminals that may appear
        first in a string derived from that symbol in the grammar.
        
        The return value is a dict, whose keys are symbols and whose values are their
        first sets.
        """
        fs = _FirstSets()
        for V in self.nonterminals:
            fs[V] = set()

        changed = False

        for rule in self:
            if not rule:
                fs[rule.lhs].add("")
                changed = True
            elif not isinstance(rule.rhs[0], Nonterminal):
                fs[rule.lhs].add(rule.rhs[0])
                changed = True

        while changed:
            changed = False

            for rule in self:
                for symbol in rule.rhs:
                    if "" not in fs[symbol]:
                        diff = fs[symbol] - {""}
                        if not diff.issubset(fs[rule.lhs]):
                            fs[rule.lhs] |= diff
                            changed = True
                        break
                else:
                    if "" not in fs[rule.lhs]:
                        fs[rule.lhs].add("")
                        changed = True
        return fs

    @lru_cache(maxsize=1)
    def follow_sets(self):
        """
        Computes the set of terminals in the grammar that may appear immediately after
        the nonterminal v in some sentential form derivable from the start symbol.
        
        The return value is a dict, whose keys are symbols and whose values are their
        follow sets.
        """
        first = self.first_sets()
        follow = {symbol: set() for symbol in self.nonterminals | self.terminals}

        follow[self.start].add("\0")

        changed = True
        while changed:
            changed = False

            for rule in self:
                end_derives_empty = True
                for i in range(len(rule.rhs)-1, -1, -1):
                    # If A -> aBC and C => "", then Follow(A) is a subset of Follow(B)
                    if end_derives_empty:
                        diff = follow[rule.lhs]
                        if not diff.issubset(follow[rule.rhs[i]]):
                            follow[rule.rhs[i]] |= diff
                            changed = True

                        if "" not in first[rule.rhs[i]]:
                            end_derives_empty = False
                    
                for i in range(len(rule.rhs) - 1):
                    # If A -> aBC, then First(C) is a subset of Follow(B)
                    diff = first[rule.rhs[i+1]] - {""}
                    if not diff.issubset(follow[rule.rhs[i]]):
                        follow[rule.rhs[i]] |= diff
                        changed = True

        return follow
    
    def _empty_productions(self):
        """
        Returns the productions of the grammar that produce the empty string.
        """
        return filter(bool, self)

    def __str__(self):
        return "CFG:\n\t" + "\n\t".join(map(str, self))
    
    def __hash__(self):
        return hash((self.start, super().__hash__()))


class _FirstSets(dict):
    """
    A dictionary of symbols and their first sets.

    This class has an overloaded `__getitem__` method so that no memory is wasted
    storing the first sets of terminals, since these are trivial to compute and complex
    grammars may have very many of them.
    """
    def __getitem__(self, key):
        if isinstance(key, Nonterminal):
            return super().__getitem__(key)
        else:
            return {key}