import copy
import unittest
from swiftsmith.semantics import SemanticNonterminal

class SNTest(SemanticNonterminal):
    required_annotations = set(["bar"])

    def __init__(self, foo):
        super().__init__()
        self.foo = foo
    
    def annotate(self, scope):
        self.annotations["bar"] = "bar"

    def string(self):
        return f"{self.foo}, {self.annotations['bar']}"

class TestSemantics(unittest.TestCase):
    def test_semantic_nonterminals_act_like_strings(self):
        a = SNTest("foo")
        self.assertEqual(str(a), "SNTest")
        self.assertEqual(a + a, "SNTestSNTest")
        self.assertEqual(" ".join([a, a]), "SNTest SNTest")
    
    def test_semantic_nonterminals_with_different_annotations_are_equal(self):
        a = SNTest("foo")
        b = SNTest("bar")
        b.annotate(None)
        self.assertEqual(a, b)
    
    def test_identical_semantic_nonterminals_are_distinct_objects(self):
        a = SNTest("foo")
        b = SNTest("foo")
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))
        self.assertNotEqual(id(a), id(b))
    
    def test_semantic_nonterminal_deep_copy_makes_new_object(self):
        a = SNTest("foo")
        b = copy.deepcopy(a)
        self.assertEqual(hash(a), hash(b))
        self.assertNotEqual(id(a), id(b))
