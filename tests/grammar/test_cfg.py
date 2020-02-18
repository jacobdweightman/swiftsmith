import unittest
import unittest.mock

from swiftsmith.grammar.cfg import Nonterminal, Production, CFG

class CFGTest(unittest.TestCase):
    def setUp(self):
        self.A = Nonterminal("A")
        self.B = Nonterminal("B")

        self.E = Nonterminal("E")
        self.T = Nonterminal("T")
        self.X = Nonterminal("X")
        self.Y = Nonterminal("Y")

        self.G = CFG(self.E, [
            Production(self.E, (self.T, self.X)),
            Production(self.T, ("(", self.E, ")")),
            Production(self.T, ("int", self.Y)),
            Production(self.X, ("+", self.E)),
            Production(self.X, ()),
            Production(self.Y, ("*", self.T)),
            Production(self.Y, ()),
        ])

    def test_nonterminals_act_like_strings(self):
        self.assertEqual(str(self.A), "A")
        self.assertEqual(self.A + self.B, "AB")
        self.assertEqual(" ".join([self.A, self.B]), "A B")
    
    def test_nonterminal_instances_with_same_str_are_equal(self):
        A1 = Nonterminal("A")
        A2 = Nonterminal("A")
        self.assertEqual(A1, A2)

    def test_productions_must_have_nonterminal_lhs(self):
        with self.assertRaises(AssertionError):
            Production("a", "asdf")

        with self.assertRaises(AssertionError):
            Production(5, "asdf")
        
        with self.assertRaises(AssertionError):
            Production([], "asdf")

    def test_identical_productions_are_equal(self):
        p1 = Production(self.A, (self.B, self.E))
        p2 = Production(self.A, (self.B, self.E))
        assert not p1 is p2
        self.assertEqual(p1, p2)
    
    def test_productions_print(self):
        p1 = Production(self.A, "a")
        self.assertEqual(str(p1), "A \u2192 a")
        p2 = Production(self.B, ("a", self.A, "b"))
        self.assertEqual(str(p2), "B \u2192 aAb")
    
    def test_empty_productions_are_falsey(self):
        p1 = Production(self.A, ())
        self.assertFalse(())
        self.assertFalse(p1)
        p2 = Production(self.A, ("a",))
        self.assertTrue(p2)

    def test_CFG_iter_preserves_order(self):
        r1 = Production(self.A, ())
        r2 = Production(self.B, ())
        r3 = Production(self.A, ())

        G = CFG(self.A, [r1, r2, r3])
        self.assertSequenceEqual(G, [r1, r2, r3])

    def test_CFG_print(self):
        # stub the string versions of the productions
        r1 = unittest.mock.MagicMock()
        r1.__str__ = lambda s: "r1"

        r2 = unittest.mock.MagicMock()
        r2.__str__ = lambda s: "r2"

        r3 = unittest.mock.MagicMock()
        r3.__str__ = lambda s: "r3"

        G = CFG(self.A, [r1, r2, r3])
        self.assertEqual(str(G), "CFG:\n\tr1\n\tr2\n\tr3")
    
    def test_CFG_hashes_dont_collide(self):
        G2 = CFG(self.T, [rule for rule in self.G])
        self.assertNotEqual(hash(G2), hash(self.G))
    
    def test_compose_CFGs(self):
        S = Nonterminal("S")
        T = Nonterminal("T")
        G = CFG(
            S,
            [
                Production(S, ("i", S)),
                Production(S, (T,)),
            ]
        )
        H = CFG(
            T,
            [
                Production(T, ("j", T)),
                Production(T, ("j",)),
            ]
        )
        self.assertEqual(G + H, CFG(
            S,
            [
                Production(S, ("i", S)),
                Production(S, (T,)),
                Production(T, ("j", T)),
                Production(T, ("j",))
            ]
        ))
