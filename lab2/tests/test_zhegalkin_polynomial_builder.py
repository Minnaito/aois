import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ZhegalkinPolynomialBuilder import ZhegalkinPolynomialBuilder
from src.TruthTableGenerator import TruthTableGenerator


class TestZhegalkinPolynomialBuilder(unittest.TestCase):
    """Тесты для ZhegalkinPolynomialBuilder"""

    def test_and_polynomial(self):
        """Тест полинома для AND"""
        tt = TruthTableGenerator("a&b")
        builder = ZhegalkinPolynomialBuilder(tt.get_truth_table(), tt.get_variables())
        polynomial = builder.get_polynomial()
        self.assertEqual(polynomial, "a&b")

    def test_or_polynomial(self):
        """Тест полинома для OR"""
        tt = TruthTableGenerator("a|b")
        builder = ZhegalkinPolynomialBuilder(tt.get_truth_table(), tt.get_variables())
        polynomial = builder.get_polynomial()
        self.assertIn("a", polynomial)
        self.assertIn("b", polynomial)
        self.assertIn("a&b", polynomial)

    def test_xor_polynomial(self):
        """Тест полинома для XOR"""
        tt = TruthTableGenerator("a^b")
        builder = ZhegalkinPolynomialBuilder(tt.get_truth_table(), tt.get_variables())
        polynomial = builder.get_polynomial()
        self.assertIn("a ⊕ b", polynomial)

    def test_not_polynomial(self):
        """Тест полинома для NOT"""
        tt = TruthTableGenerator("!a")
        builder = ZhegalkinPolynomialBuilder(tt.get_truth_table(), tt.get_variables())
        polynomial = builder.get_polynomial()
        self.assertIn("1 ⊕ a", polynomial)

    def test_implication_polynomial(self):
        """Тест полинома для импликации"""
        tt = TruthTableGenerator("a->b")
        builder = ZhegalkinPolynomialBuilder(tt.get_truth_table(), tt.get_variables())
        polynomial = builder.get_polynomial()
        # a->b = 1 ⊕ a ⊕ a&b
        self.assertIn("1", polynomial)
        self.assertIn("a", polynomial)
        self.assertIn("a&b", polynomial)

    def test_equivalence_polynomial(self):
        """Тест полинома для эквивалентности"""
        tt = TruthTableGenerator("a~b")
        builder = ZhegalkinPolynomialBuilder(tt.get_truth_table(), tt.get_variables())
        polynomial = builder.get_polynomial()
        self.assertIn("1 ⊕ a ⊕ b", polynomial)

    def test_constant_zero_polynomial(self):
        """Тест полинома для константы 0"""
        tt = TruthTableGenerator("a&!a")
        builder = ZhegalkinPolynomialBuilder(tt.get_truth_table(), tt.get_variables())
        polynomial = builder.get_polynomial()
        self.assertEqual(polynomial, "0")

    def test_constant_one_polynomial(self):
        """Тест полинома для константы 1"""
        tt = TruthTableGenerator("a|!a")
        builder = ZhegalkinPolynomialBuilder(tt.get_truth_table(), tt.get_variables())
        polynomial = builder.get_polynomial()
        self.assertEqual(polynomial, "1")

    def test_three_variables_polynomial(self):
        """Тест полинома для трех переменных"""
        tt = TruthTableGenerator("a&b&c")
        builder = ZhegalkinPolynomialBuilder(tt.get_truth_table(), tt.get_variables())
        polynomial = builder.get_polynomial()
        self.assertEqual(polynomial, "a&b&c")


if __name__ == '__main__':
    unittest.main()