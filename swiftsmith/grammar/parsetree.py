from swiftsmith.grammar.cfg import Nonterminal

class Tree(object):
    """A data structure representing a hierarchical collection."""

    def __init__(self, value, *args):
        self.parent = None

        if len(args) == 0:
            self.children = None
        elif len(args) == 1:
            self.children = []
            for child in args[0]:
                if not isinstance(child, Tree):
                    # child should be the same kind of tree as self; using type(self)
                    # matches the type of self and its children.
                    child = type(self)(child)
                self.children.append(child)
                child.parent = self
        else:
            raise TypeError("Tree.__init__ takes a value and optionally a sequence of "
                            "its children,  but more arguments were given.")
        self.value = value
    
    def add_child(self, child):
        """Adds a new rightmost child to this tree."""
        if self.children is None:
            self.children = []
        if not isinstance(child, type(self)):
            child = type(self)(child)
        self.children.append(child)
        child.parent = self
    
    def ancestors(self):
        """Generate the ancestors of the current node."""
        node = self.parent
        while node:
            yield node
            node = node.parent
    
    def childwhere(self, matcher):
        """returns the first child of this tree where matcher returns True"""
        return next(filter(matcher, self.children))

    def isleaf(self):
        """True if this tree does not have children."""
        return self.children is None
    
    def preorder(self):
        """A generator of the preorder traversal of this tree."""
        yield self.value
        if self.children:
            for child in self.children:
                yield from child.preorder()
    
    def postorder(self):
        """A generator of the postorder traversal of this tree."""
        if self.children:
            for child in self.children:
                yield from child.postorder()
        yield self.value
    
    def __contains__(self, value):
        """
        A tree contains a value iff it is equal to it or one of its descendents' values.
        """
        for item in self:
            if value == item:
                return True
        return False

    def __iter__(self):
        yield from self.preorder()

    def __str__(self):
        if self.children:
            return "(" + str(self.value) + " " + " ".join(map(str, self.children))  + ")"
        else:
            return str(self.value)
    
    def __repr__(self):
        return str(self)


class ParseTree(Tree):
    """
    The data structure that represents a successful parse of a string in a context-free
    grammar.
    """

    def __init__(self, value, *args):
        super().__init__(value, *args)
    
        if len(args) == 0:
            if isinstance(value, Nonterminal):
                self.frontier = [self]
            else:
                self.frontier = []
        else:
            self.frontier = []
            for child in self.children:
                self.frontier.extend(child.frontier)
                child.parent = self

    
    def leftmost_unexpanded_nonterminal(self):
        """
        Find and return the leftmost nonterminal in the tree that has not been expanded.

        This is the next nonterminal to be rewritten in a leftmost derivation.
        """
        return self.frontier[0]
    
    def rightmost_unexpanded_nonterminal(self):
        """
        Find and return the rightmost nonterminal in the tree that has not been
        expanded.

        This is the next nonterminal to be rewritten in a rightmost derivation.
        """
        return self.frontier[-1]
    
    def isunexpanded(self):
        """
        An unexpanded tree contains a nonterminal and has undefined children.

        An unexpanded subtree may be expanded using a production from a grammar.
        """
        return isinstance(self.value, Nonterminal) and self.children is None
    
    def expand(self, children):
        """
        Sets the children of this tree to the given iterable, and updates the frontiers
        of of the tree.
        """
        assert self.isunexpanded(), "Attempted to expand an already expanded node."

        self.children = []
        self.frontier = []
        for child in children:
            if not isinstance(child, type(self)):
                # child should be the same kind of tree as self; using type(self) allows
                # ParseTree to be subclassed.
                child = type(self)(child)
            self.children.append(child)
            self.frontier.extend(child.frontier)
            child.parent = self
        
        for node in self.ancestors():
            i = node.frontier.index(self)
            node.frontier[i:i+1] = self.frontier
    
    def string(self):
        """
        Get the string of terminals represented by this parse tree.
        """
        if self.isleaf():
            return str(self.value)
        return "".join(child.string() for child in self.children)
