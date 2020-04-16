from swiftsmith.enum import Case, case_statements, Enum, EnumDeclaration
from swiftsmith.expression import Expression
from swiftsmith.formatting import EOL
from swiftsmith.metamorphic import failable_initializer
from swiftsmith.semantics import SemanticParseTree
from swiftsmith.standard_library import Int
from swiftsmith.statement import statement
from swiftsmith.types import EnumType

import unittest

class FailableInitTests(unittest.TestCase):
    def test_failable_initializer(self):
        A = EnumType("A")
        A.add_case("b", [])
        tree = SemanticParseTree(statement, [
            SemanticParseTree(EnumDeclaration(), [
                "enum ",
                Enum(),
                " {",
                EOL(),
                SemanticParseTree(case_statements, ["case ", Case()]),
                EOL(),
                "}"
            ]),
            Expression(A)
        ])
        tree.annotate()
        failable_initializer(tree)
        self.assertEqual(
            "enum A {\n\tinit?() { self = A.b }\n\n\tcase b\n}.init()!",
            tree.string()
        )
