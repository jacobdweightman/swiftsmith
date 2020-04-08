import unittest
import unittest.mock

from swiftsmith.enum import Case, Enum, statements
from swiftsmith.formatting import Block
from swiftsmith.semantics import Scope, SemanticParseTree
from swiftsmith.types import EnumType, DataType

class EnumTests(unittest.TestCase):
    def test_build_enum(self):
        A = EnumType("A")
        A.add_case("a", [])
        A.add_case("b", [])
        A.add_case("c", [])
        self.assertEqual(len(A.cases), 3)
    
    def test_get_enum_expression(self):
        A = EnumType("A")
        A.add_case("a", [])
        self.assertEqual(A.newvalue(), "A.a")
    
    def test_get_enum_expression_with_inferred_type(self):
        A = EnumType("A")
        A.add_case("a", [])
        self.assertEqual(A.newvalue(type_inferred=True), ".a")
    
    def test_get_enum_expression_with_associated_value(self):
        A = EnumType("A")
        av = DataType("AV")
        av.newvalue = unittest.mock.MagicMock(return_value="3")
        A.add_case("a", [av])
        self.assertEqual(A.newvalue(), "A.a(3)")
    
    def test_get_enum_expression_with_generics(self):
        generictype = DataType("GT")
        A = EnumType("A", generic_types={generictype: None})
        A.add_case("a", [generictype])
        concretetype = DataType("CT")
        concretetype.newvalue = unittest.mock.MagicMock(return_value="concrete")
        self.assertEqual(
            A.specialize(GT=concretetype).newvalue(),
            "A<CT>.a(concrete)"
        )
    
    def test_get_enum_expression_with_too_few_generics_throws(self):
        generictype = DataType("GT")
        A = EnumType("A", generic_types={generictype: None})
        A.add_case("a", [generictype])
        with self.assertRaises(AssertionError):
            A.newvalue()

    def test_enum_in_scope(self):
        outer_scope = Scope()
        tree = SemanticParseTree("enum", [
            Enum(),
            SemanticParseTree(statements, [
                Case(),
                Case(),
            ])
        ])
        
        tree.annotate(scope=outer_scope)
        self.assertEqual(len(outer_scope.children), 1)
        enumscope = outer_scope.children[0]
        enumtype = enumscope.value
        self.assertEqual(len(enumtype.cases), 2)
        self.assertIn(enumtype, outer_scope.accessible_types())
