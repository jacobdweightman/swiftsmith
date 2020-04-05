import unittest
from swiftsmith.access import AccessModifier
from swiftsmith.function import Function, FuncDeclaration, block, Block
from swiftsmith.scope import Scope
from swiftsmith.semantics import SemanticParseTree, Token

class Interceptor(Token):
    def __init__(self, testclosure):
        self.testclosure = testclosure
    
    def annotate(self, scope, context):
        self.testclosure(scope, context)


class TestFunction(unittest.TestCase):
    def test_function_parameters_in_scope(self):
        outer_scope = Scope()
        function = Function()
        interceptor = Interceptor(None)
        tree = SemanticParseTree(FuncDeclaration(), [
            function,
            SemanticParseTree(block, [
                Block(),
                interceptor
            ])
        ])

        def testclosure(inner_scope: Scope, context):
            arguments = function.annotations["arguments"]
            self.assertGreater(len(arguments), 0, "useless test")
            for argument in arguments:
                self.assertIsNotNone(inner_scope.choose_variable(name=argument))
            
        interceptor.testclosure = testclosure
        tree.annotate(scope=outer_scope)
    
    def test_access_modifier_changes_function_access_level(self):
        funcdeclaration = FuncDeclaration()
        modifier = AccessModifier()
        tree = SemanticParseTree(funcdeclaration, [modifier])
        tree.annotate()
        self.assertEqual(
            funcdeclaration.annotations["access"],
            modifier.annotations["access"]
        )

