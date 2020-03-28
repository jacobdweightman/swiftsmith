import copy
import unittest
from swiftsmith.statement import Assignment, Declaration
from swiftsmith.scope import Scope
from swiftsmith.semantics import SemanticParseTree
from swiftsmith.standard_library import Int
from swiftsmith.swift import swift

class TestStatement(unittest.TestCase):
    def test_declaration_adds_variable_to_scope_later(self):
        scope = Scope()
        dec = Declaration(Int)
        subtree = SemanticParseTree(dec)
        tree = SemanticParseTree(Assignment(None), [subtree])
        dec.annotate(scope, subtree)
        self.assertEqual(len(scope.variables), 0)
        tree._run_deferred()
        self.assertEqual(len(scope.variables), 1)
    
    def test_deep_copy_assignments_are_equal(self):
        assignment1 = Assignment(None)
        assignment2 = copy.deepcopy(assignment1)
        self.assertNotEqual(id(assignment1), id(assignment2))
        self.assertEqual(assignment1, assignment2)
        self.assertEqual(hash(assignment2), hash(assignment2))
