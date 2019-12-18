import unittest
from swiftsmith.grammar.cfg import Nonterminal, Production, CFG
from swiftsmith.grammar.lr0 import LR_Item

class LR0Test(unittest.TestCase):
    def setUp(self):
        self.S = Nonterminal("S")
        self.P1 = Production(self.S, (self.S, "a"))
        self.P2 = Production(self.S, ("a",))
        self.G = CFG(
            self.S,
            [
                self.P1,
                self.P2
            ]
        )
    
    def test_lr0_item_str(self):
        item = LR_Item(self.P1, 0)
        self.assertEqual(str(item), "S \u2192 .Sa")
        item = LR_Item(self.P1, 1)
        self.assertEqual(str(item), "S \u2192 S.a")
        item = LR_Item(self.P1, 2)
        self.assertEqual(str(item), "S \u2192 Sa.")
    
    def test_lr0_item_next(self):
        item = LR_Item(self.P1, 0)
        self.assertEqual(next(item), self.S)
        item = LR_Item(self.P1, 1)
        self.assertEqual(next(item), "a")
        item = LR_Item(self.P1, 2)
        with self.assertRaises(StopIteration):
            next(item)
