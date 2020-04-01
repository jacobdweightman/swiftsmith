import unittest
from swiftsmith import Scope
from swiftsmith.types import EnumType, FunctionType
from swiftsmith.standard_library import Bool, Int

class ScopeTests(unittest.TestCase):
    def test_declared_variable_is_accessible(self):
        scope = Scope()
        scope.declare("foo", Int, False)
        self.assertSetEqual(set(scope.accessible_variables()), {("foo", Int, False)})
    
    def test_declared_function_is_accessible(self):
        scope = Scope()
        scope.declare_func("foo", {"x": Int}, Int)
        self.assertDictEqual(
            scope.accessible_functions(),
            {
                "foo": FunctionType({"x": Int}, Int),
            }
        )
    
    def test_nested_type_is_accessible(self):
        A = EnumType("A")
        scope = Scope()
        scope.add_child(Scope(datatype=A))
        self.assertSetEqual(set(scope.accessible_types()), {A})
    
    def test_deeply_nested_type_is_accessible(self):
        A = EnumType("A")
        scope = Scope()
        scope.add_child(Scope())
        scope.children[0].add_child(Scope())
        scope.children[0].children[0].add_child(Scope())
        scope.children[0].children[0].children[0].add_child(Scope(datatype=A))
        self.assertSetEqual(set(scope.accessible_types()), {A})
    
    def test_enclosing_type_is_accessible(self):
        A = EnumType("A")
        parent = Scope(datatype=A)
        child = Scope()
        parent.add_child(child)
        self.assertSetEqual(set(child.accessible_types()), {A})
    
    def test_enclosing_sibling_type_is_accessible(self):
        A = EnumType("A")
        grandparent = Scope()
        parent = Scope()
        grandparent.add_child(parent)
        uncle = Scope(datatype=A)
        grandparent.add_child(uncle)
        child = Scope()
        parent.add_child(child)
        self.assertSetEqual(set(child.accessible_types()), {A})
    
    def test_importing_standard_library_exposes_expected_values(self):
        scope = Scope()
        scope.import_standard_library()
        self.assertSetEqual(set(scope.accessible_types()), {Bool, Int})
        self.assertSetEqual(
            set(scope.accessible_functions().keys()),
            {"&+", "&*", ">", "=="},
        )
        self.assertSetEqual(set(scope.accessible_variables()), set())
