import unittest
from swiftsmith import Scope
from swiftsmith.types import AccessLevel, DataType, EnumType, FunctionType

class DataTypeTests(unittest.TestCase):
    def test_get_full_name(self):
        A = DataType("A")
        self.assertEqual(A.full_name(), "A")
    
    def test_get_full_name_with_generic(self):
        GT = DataType("GT")
        A = DataType("A", generic_types={GT: None})
        self.assertEqual(A.full_name(), "A<GT>")
    
    def test_get_full_name_with_specialized_generic(self):
        GT = DataType("GT")
        CT = DataType("CT")
        A = DataType("A", generic_types={GT: CT})
        self.assertEqual(A.full_name(), "A<CT>")
