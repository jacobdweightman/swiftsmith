from swiftsmith.expression import Expression
from swiftsmith.metamorphic import unnecessary_addition, unnecessary_multiplication
from swiftsmith.semantics import SemanticParseTree
from swiftsmith.standard_library import Int

import unittest

class UnnecessaryArithmeticTests(unittest.TestCase):
    def test_unnecessary_addition(self):
        tree = SemanticParseTree(Expression(Int))
        tree.annotate()
        original = tree.string()
        unnecessary_addition(tree)
        self.assertEqual(tree.string(), f"({original}) + 0")
    
    def test_unnecessary_multiplication(self):
        tree = SemanticParseTree(Expression(Int))
        tree.annotate()
        original = tree.string()
        unnecessary_multiplication(tree)
        self.assertEqual(tree.string(), f"({original}) * 1")
