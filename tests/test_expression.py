import unittest
from swiftsmith.expression import expression_grammar, Variable, Int, Bool
from swiftsmith.scope import Scope
from swiftsmith.semantics import SemanticParseTree

class TestExpression(unittest.TestCase):
    def test_variable_resolves_in_scope(self):
        scope = Scope()
        scope.declare("foo", "Int", False)
        v = Variable("Int")
        v.annotate(scope, None)
        self.assertEqual(v.string(), "foo")
    
    def test_variable_falls_back_to_literal(self):
        v = Variable("Int")
        v.annotate(Scope(), None)
        int(v.string()) # ValueError if it didn't fall back to an int literal
    
    def test_variable_annotated_by_tree(self):
        scope = Scope()
        scope.declare("foo", "Int", False)
        tree = SemanticParseTree(Variable("Int"))
        tree.annotate(scope=scope)
        self.assertEqual(tree.string(), "foo")
    
    def test_bool_annotated_by_tree(self):
        tree = SemanticParseTree(Bool())
        tree.annotate()
        self.assertIn(tree.string(), ["true", "false"])
