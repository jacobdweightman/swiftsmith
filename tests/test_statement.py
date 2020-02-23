import unittest
from swiftsmith.statement import Declaration
from swiftsmith.scope import Scope
from swiftsmith.semantics import SemanticParseTree

class TestStatement(unittest.TestCase):
    def test_declaration_adds_variable_to_scope_later(self):
        scope = Scope()
        dec = Declaration("Int")
        subtree = SemanticParseTree(dec)
        tree = SemanticParseTree("parent", [subtree])
        dec.annotate(scope, subtree)
        self.assertEqual(len(scope.variables), 0)
        tree._run_deferred()
        self.assertEqual(len(scope.variables), 1)
