import unittest
from swiftsmith.statement import Declaration
from swiftsmith.scope import Scope

class TestStatement(unittest.TestCase):
    def test_declaration_adds_variable_to_scope(self):
        scope = Scope()
        dec = Declaration("Int")
        scope.push_deferred()
        dec.annotate(scope)
        self.assertEqual(len(scope.variables), 0)
        scope.pop_deferred()
        self.assertEqual(len(scope.variables), 1)
