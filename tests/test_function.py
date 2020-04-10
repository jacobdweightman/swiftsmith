import unittest
from swiftsmith.function import Function, FuncDeclaration, block, Block
from swiftsmith.modifier import AccessModifier, BindingModifier
from swiftsmith.scope import Scope
from swiftsmith.semantics import SemanticParseTree, Token
from swiftsmith.standard_library import Int
from swiftsmith.types import AccessLevel, Binding, DataType, FunctionType

class Interceptor(Token):
    def __init__(self, testclosure):
        self.testclosure = testclosure
    
    def annotate(self, scope, context):
        self.testclosure(scope, context)


class TestFunction(unittest.TestCase):
    def test_function_full_name(self):
        GT = DataType("GT")
        ftype = FunctionType(AccessLevel.internal, {"a": GT}, GT)
        self.assertEqual(ftype.full_name(), "(a: GT) -> GT")
    
    def test_function_parameters_in_scope(self):
        outer_scope = Scope()
        outer_scope.add_child(Scope(None, Int))
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
    
    def test_static_function_declared_static(self):
        T = DataType("T")
        scope = Scope(None, T)
        funcdeclaration = FuncDeclaration(binding=Binding.static)
        tree = SemanticParseTree(funcdeclaration, [
            BindingModifier(),
            Function(),
            SemanticParseTree(block, [Block()])
        ])
        tree.annotate(scope=scope)
        declaration = tree.string()
        self.assertTrue(declaration.startswith("static"))
    
    def test_static_function_foo(self):
        pass
