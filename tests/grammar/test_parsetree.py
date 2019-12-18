import unittest
from swiftsmith.grammar.cfg import Nonterminal
from swiftsmith.grammar.parsetree import ParseTree

class ParseTreeTest(unittest.TestCase):
    def setUp(self):
        self.A = Nonterminal("A")
        self.B = Nonterminal("B")
        self.t1 = ParseTree(self.A)
        self.t2 = ParseTree(self.A)
        self.t3 = ParseTree(self.B)
        self.t4 = ParseTree(self.A, [self.t2, ParseTree("a"), self.t3])
        self.t = ParseTree(
            self.A,
            [
                ParseTree("a"),
                self.t1,
                self.t4
            ]
        )

    def test_isleaf(self):
        a = ParseTree(5)
        self.assertTrue(a.isleaf())
        b = ParseTree(4, [ParseTree(6)])
        self.assertFalse(b.isleaf())
    
    def test_preorder(self):
        a = ParseTree(1, [ParseTree(2), ParseTree(3, [ParseTree(4)]), ParseTree(5)])
        for i,j in zip(a.preorder(), [1, 2, 3, 4, 5]):
            self.assertEqual(i, j)
    
    def test_postorder(self):
        a = ParseTree(1, [ParseTree(2), ParseTree(3, [ParseTree(4)]), ParseTree(5)])
        for i,j in zip(a.postorder(), [2, 4, 3, 5, 1]):
            self.assertEqual(i, j)
    
    def test_parent(self):
        self.assertEqual(self.t1.parent, self.t)
        self.assertEqual(self.t2.parent, self.t4)
        self.assertEqual(self.t3.parent, self.t4)
    
    def test_ancestors(self):
        self.assertSequenceEqual(list(self.t2.ancestors()), [self.t4, self.t])

    def test_rightleft_unexpanded_nonterminal(self):
        self.assertEqual(self.t.leftmost_unexpanded_nonterminal(), self.t1)
        self.assertEqual(self.t.rightmost_unexpanded_nonterminal(), self.t3)
    
