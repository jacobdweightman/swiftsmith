import unittest
from swiftsmith import Scope
from swiftsmith.types import AccessLevel, DataType, EnumType, FunctionType
from swiftsmith.standard_library import Bool, Int, Optional

class ScopeTests(unittest.TestCase):
    def test_declared_variable_is_accessible(self):
        scope = Scope()
        scope.declare("foo", Int, False)
        self.assertSetEqual(set(scope.accessible_variables()), {("foo", Int, False)})
    
    def test_declared_function_is_accessible(self):
        scope = Scope()
        scope.declare_func(AccessLevel.internal, "foo", {"x": Int}, Int)
        self.assertDictEqual(
            scope.accessible_functions(),
            {
                "foo": FunctionType(AccessLevel.internal, {"x": Int}, Int),
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
    
    def test_accessible_types_access_level_filter(self):
        A = EnumType("A", access=AccessLevel.public)
        B = EnumType("B", access=AccessLevel.internal)
        C = EnumType("C", access=AccessLevel.fileprivate)
        root = Scope()
        root.add_child(Scope(None, A))
        root.add_child(Scope(None, B))
        root.add_child(Scope(None, C))
        self.assertSetEqual(
            set(root.accessible_types(at_least=AccessLevel.fileprivate)),
            {A, B, C}
        )
        self.assertSetEqual(
            set(root.accessible_types(at_least=AccessLevel.internal)),
            {A, B}
        )
        self.assertSetEqual(
            set(root.accessible_types(at_least=AccessLevel.public)),
            {A}
        )
    
    def test_accessible_types_include_self_filter(self):
        A = EnumType("A")
        root = Scope(datatype=A)
        self.assertSetEqual(set(root.accessible_types()), set())
        self.assertSetEqual(set(root.accessible_types(include_self=False)), set())
        self.assertSetEqual(set(root.accessible_types(include_self=True)), {A})

    def test_importing_standard_library_exposes_expected_values(self):
        scope = Scope()
        scope.import_standard_library()
        self.assertSetEqual(set(scope.accessible_types()), {Bool, Int, Optional})
        self.assertSetEqual(
            set(scope.accessible_functions().keys()),
            {"&+", "&*", ">", "=="},
        )
        self.assertSetEqual(set(scope.accessible_variables()), set())
    
    def test_accessible_functions_access_level_filter(self):
        scope = Scope()
        scope.declare_func(AccessLevel.public, "foo", {}, Int)
        scope.declare_func(AccessLevel.internal, "bar", {}, Int)
        scope.declare_func(AccessLevel.private, "baz", {}, Int)
        self.assertSetEqual(
            set(scope.accessible_functions(at_least=AccessLevel.public).keys()),
            {"foo"}
        )
        self.assertSetEqual(
            set(scope.accessible_functions(at_least=AccessLevel.internal).keys()),
            {"foo", "bar"}
        )
        self.assertSetEqual(
            set(scope.accessible_functions(at_least=AccessLevel.private).keys()),
            {"foo", "bar", "baz"}
        )

    def test_accessible_functions_hides_private_static_methods(self):
        root = Scope()
        A = DataType("A", static_methods={
            "a": FunctionType(AccessLevel.private, {}, Int),
            "b": FunctionType(AccessLevel.fileprivate, {}, Int),
        })
        root.add_child(Scope(datatype=A))
        self.assertSetEqual({"A.b"}, set(root.accessible_functions().keys()))
    
    def test_specialize_generic_type(self):
        scope = Scope()
        GT = DataType("GT")
        A = DataType("A", access=AccessLevel.internal)
        scope.add_child(Scope(None, A))
        B = DataType("B", generic_types={GT: None})
        self.assertDictEqual(scope.specialize_type(B).generic_types, {GT: A})
    
    def test_specialize_generic_type_filter(self):
        scope = Scope()
        GT = DataType("GT")
        A = DataType("A", access=AccessLevel.internal)
        B = DataType("B", access=AccessLevel.public)
        scope.add_child(Scope(None, A))
        scope.add_child(Scope(None, B))
        C = DataType("C", generic_types={GT: None})
        self.assertDictEqual(
            scope.specialize_type(C, at_least=AccessLevel.public).generic_types,
            {GT: B}
        )
