import unittest
from swiftsmith import Scope

class ScopeTests(unittest.TestCase):
    def test_declared_variables_may_be_chosen(self):
        scope = Scope()
        scope.declare("foo", "Int", False)
        self.assertEqual(scope.choose_variable(), "foo")
    
    def test_declared_functions_may_be_chosen(self):
        scope = Scope()
        scope.declare_func("foo", {"x": "Int"}, "Int")
        self.assertEqual(scope.choose_function(), ("foo", {"x": "Int"}, "Int"))
    
    def test_deferred_actions_run_when_popped(self):
        scope = Scope()
        x = 0
        scope.push_deferred()
        def closure():
            nonlocal x
            x += 1
        scope.defer(closure)
        self.assertEqual(x, 0)
        scope.pop_deferred()
        self.assertEqual(x, 1)

    def test_deferred_actions_run_in_reverse_order(self):
        scope = Scope()
        x = 0
        scope.push_deferred()
        def closure1():
            nonlocal x
            x *= 2
        scope.defer(closure1)
        def closure2():
            nonlocal x
            x += 1
        scope.defer(closure2)

        # If closure1 runs first, then x == (0*2)+1 which is 1.
        # If closure2 runs first, then x == (0+1)*2 which is 2.
        self.assertEqual(x, 0)
        scope.pop_deferred()
        self.assertEqual(x, 2)
    
    def test_mutiple_deferred_stacks_dont_interfere(self):
        scope = Scope()
        x = 0
        def closure():
            nonlocal x
            x += 1
        
        scope.push_deferred()
        scope.defer(closure)
        scope.push_deferred()
        scope.defer(closure)
        
        self.assertEqual(x, 0)
        scope.pop_deferred()
        self.assertEqual(x, 1)
        scope.pop_deferred()
        self.assertEqual(x, 2)
