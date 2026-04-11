import unittest
from src.ZhegalkinPolynomialBuilder import ZhegalkinPolynomialBuilder
from src.TruthTable import TruthTable
from src.ExpressionParser import BooleanExpressionParser


class TestZhegalkinPolynomialBuilder(unittest.TestCase):
    def setUp(self):
        self.parser = BooleanExpressionParser()

    def _build(self, expr, variables):
        tt = TruthTable(variables, expr, self.parser)
        truth_table_list = [{'inputs': bits, 'output': res} for bits, res in tt]
        return ZhegalkinPolynomialBuilder(truth_table_list, variables)

    def test_and_gate(self):
        builder = self._build("a&b", ['a','b'])
        self.assertEqual(builder.get_polynomial(), "ab")

    def test_or_gate(self):
        builder = self._build("a|b", ['a','b'])
        # порядок может быть a ^ b ^ ab или b ^ a ^ ab
        self.assertIn(builder.get_polynomial(), ["a ⊕ b ⊕ ab", "b ⊕ a ⊕ ab"])

    def test_not_gate(self):
        builder = self._build("!a", ['a'])
        self.assertEqual(builder.get_polynomial(), "1 ⊕ a")


    def test_constant_zero(self):
        builder = self._build("0", [])
        self.assertEqual(builder.get_polynomial(), "0")

    def test_constant_one(self):
        builder = self._build("1", [])
        self.assertEqual(builder.get_polynomial(), "1")

    def test_complex_expression(self):
        builder = self._build("a->b", ['a','b'])
        self.assertEqual(builder.get_polynomial(), "1 ⊕ a ⊕ ab")

    def test_print_polynomial(self):
        builder = self._build("a&b", ['a','b'])
        builder.print_polynomial()


if __name__ == '__main__':
    unittest.main()
