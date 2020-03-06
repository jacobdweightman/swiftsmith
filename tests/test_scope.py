import unittest
from swiftsmith import Scope
from swiftsmith.types import Int

class ScopeTests(unittest.TestCase):
    def test_declared_variables_may_be_chosen(self):
        scope = Scope()
        scope.declare("foo", Int, False)
        self.assertEqual(scope.choose_variable(), "foo")
    
    def test_declared_functions_may_be_chosen(self):
        scope = Scope()
        scope.declare_func("foo", {"x": Int}, Int)
        self.assertEqual(scope.choose_function(), ("foo", {"x": Int}, Int))
