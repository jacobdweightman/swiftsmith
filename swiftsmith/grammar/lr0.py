class LR_Item(object):
    """
    Represents an intermediate parse of a production.

    LR items are used to construct the parse table of an LR(k) parser. Given a
    production A -> abcd, at the start of the parse the state is represented with an LR
    item A -> .abcd and after reading an `a` it is A -> a.bcd
    """

    def __init__(self, production, index):
        self.production = production
        self.index = index
    
    def __next__(self):
        try:
            return self.production.rhs[self.index]
        except IndexError:
            raise StopIteration
    
    def __str__(self):
        head = "".join(map(str, self.production.rhs[:self.index]))
        tail = "".join(map(str, self.production.rhs[self.index:]))
        return self.production.lhs + " \u2192 " + head + "." + tail

class LR0Parser(object):
    """
    Represents a LR(0) parser.

    An LR(0) parser is constructed from a context-free grammar. The LR(0) parsing
    algorithm first constructs a "parse table", and this parse table is then used to
    parse strings in the grammar (if the grammar is LR(0)) in linear time.
    """

    def __init__(self, G):
        pass

    def _closure(self, grammar, production):
        items = set()
        stack = [LR_Item(production, 0)]

        while len(stack) > 0:
            item = stack.pop()
            items.add(item)

            for production in grammar.productions:
                if production.lhs == item.production.rhs[item.index]:
                    stack.append(LR_Item(production, 0))
        
        return frozenset(items)
