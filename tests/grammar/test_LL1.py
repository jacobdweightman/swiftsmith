import unittest
from swiftsmith.grammar.cfg import Nonterminal, Production, CFG
from swiftsmith.grammar.ll1 import LL1Parser

class LL1Test(unittest.TestCase):
    def setUp(self):
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

        self.parser = LL1Parser(self.G)

    def test_table_construction(self):
        self.assertDictEqual(self.parser.table, {
            (self.E, "("):      (self.T, self.X),
            (self.E, "int"):    (self.T, self.X),
            (self.T, "("):      ("(", self.E, ")"),
            (self.T, "int"):    ("int", self.Y),
            (self.X, ")"):      (),
            (self.X, "+"):      ("+", self.E),
            (self.X, "\0"):     (),
            (self.Y, ")"):      (),
            (self.Y, "+"):      (),
            (self.Y, "*"):      ("*", self.T),
            (self.Y, "\0"):      (),
        })
    
    def test_parse(self):
        self.assertTrue(self.parser.parse(("int", "*", "int")))
        self.assertTrue(self.parser.parse(("int", "*", "(", "int", "+", "int", ")")))
        self.assertFalse(self.parser.parse(("(", "int", "+", "int", ")", "*", "int")))
