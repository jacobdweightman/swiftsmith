import copy
import unittest
from swiftsmith.expression import Expression, Value, Variable
from swiftsmith.grammar import Nonterminal
from swiftsmith.scope import Scope
from swiftsmith.semantics import SemanticParseTree, SemanticNonterminal
from swiftsmith.standard_library import Bool, Int

class TestExpression(unittest.TestCase):
    def test_variable_resolves_in_scope(self):
        scope = Scope()
        scope.declare("foo", Int, False)
        v = Variable(Int)
        v.annotate(scope, None)
        self.assertEqual(v.string(), "foo")
    
    def test_variable_falls_back_to_literal(self):
        v = Variable(Int)
        v.annotate(Scope(), None)
        int(v.string()) # ValueError if it didn't fall back to an int literal
    
    def test_variable_annotated_by_tree(self):
        scope = Scope()
        scope.declare("foo", Int, False)
        tree = SemanticParseTree(Variable(Int))
        tree.annotate(scope=scope)
        self.assertEqual(tree.string(), "foo")
    
    def test_bool_annotated_by_tree(self):
        tree = SemanticParseTree(Value(Bool))
        tree.annotate()
        self.assertIn(tree.string(), ["true", "false"])
    
    def test_deep_copy_expression_tokens_are_equal(self):
        intexp = Expression(Int)
        intexp2 = copy.deepcopy(intexp)
        self.assertEqual(intexp, intexp2)
    
    def test_expression_infers_type_from_ancestors(self):
        class A(SemanticNonterminal):
            def __init__(self, datatype):
                self.datatype = datatype
            def annotate(self, scope, context):
                pass
        
        exp = Expression(None)
        tree = SemanticParseTree(A(Int), [exp])
        tree.annotate()
        self.assertEqual(exp.datatype, Int)

        exp = Expression(None)
        tree = SemanticParseTree(A(Bool), [
            SemanticParseTree(Nonterminal("foo"), [exp])
        ])
        tree.annotate()
        self.assertEqual(exp.datatype, Bool)

        exp = Expression(None)
        tree = SemanticParseTree(A(Int), [
            SemanticParseTree(Nonterminal("foo"), [
                SemanticParseTree(Nonterminal("foo"), [exp])
            ])
        ])
        tree.annotate()
        self.assertEqual(exp.datatype, Int)
