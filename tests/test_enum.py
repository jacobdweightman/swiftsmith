import unittest
from swiftsmith.enum import Case, Enum
from swiftsmith.formatting import Block
from swiftsmith.semantics import Scope, SemanticParseTree
from swiftsmith.types import EnumType, Int

class EnumTests(unittest.TestCase):
    def test_build_enum(self):
        A = EnumType("A")
        A.add_case("a")
        A.add_case("b")
        A.add_case("c")
        self.assertEqual(len(A.cases), 3)
    
    def test_get_enum_expression(self):
        A = EnumType("A")
        A.add_case("a")
        self.assertEqual(A.choose_case_value(), "A.a")

    def test_get_enum_case_by_raw_value(self):
        A = EnumType("A", raw_type=Int)
        A.add_case("a", raw_value=1)
        self.assertEqual(A.case_with_raw_value(1), "A.a")
    
    def test_enum_in_scope(self):
        outer_scope = Scope()
        tree = SemanticParseTree("enum", [
            Enum(),
            Case(),
            Case(),
        ])
        
        tree.annotate(scope=outer_scope)
        self.assertEqual(len(outer_scope.children), 1)
        enumscope = outer_scope.children[0]
        enumtype = enumscope.value
        self.assertEqual(len(enumtype.cases), 2)

        # TODO: how to read which enums are in scope of enclosing?
