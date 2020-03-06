import unittest
from swiftsmith import Scope
from swiftsmith.types import EnumType, Int

class ScopeTests(unittest.TestCase):
    def test_declared_variables_may_be_chosen(self):
        scope = Scope()
        scope.declare("foo", Int, False)
        self.assertEqual(scope.choose_variable(), "foo")
    
    def test_declared_functions_may_be_chosen(self):
        scope = Scope()
        scope.declare_func("foo", {"x": Int}, Int)
        self.assertEqual(scope.choose_function(), ("foo", {"x": Int}, Int))
    
    def test_may_choose_nested_type(self):
        A = EnumType("A")
        scope = Scope()
        scope.add_child(Scope(datatype=A))
        self.assertEqual(scope.choose_type(), A)
    
    def test_may_choose_deeply_nested_type(self):
        A = EnumType("A")
        scope = Scope()
        scope.add_child(Scope())
        scope.children[0].add_child(Scope())
        scope.children[0].children[0].add_child(Scope())
        scope.children[0].children[0].children[0].add_child(Scope(datatype=A))
        self.assertEqual(scope.choose_type(), A)
    
    def test_may_choose_enclosing_type(self):
        A = EnumType("A")
        parent = Scope(datatype=A)
        child = Scope()
        parent.add_child(child)
        self.assertEqual(child.choose_type(), A)
    
    def test_may_choose_enclosing_sibling_type(self):
        A = EnumType("A")
        grandparent = Scope()
        parent = Scope()
        grandparent.add_child(parent)
        uncle = Scope(datatype=A)
        grandparent.add_child(uncle)
        child = Scope()
        parent.add_child(child)
        self.assertEqual(child.choose_type(), A)

