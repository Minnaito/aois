import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.BooleanDerivativeCalculator import BooleanDerivativeCalculator
from src.TruthTableGenerator import TruthTableGenerator


class TestBooleanDerivativeCalculator(unittest.TestCase):
    """Тесты для BooleanDerivativeCalculator"""

    def setUp(self):
        self.tt_and = TruthTableGenerator("a&b")
        self.calc_and = BooleanDerivativeCalculator(
            self.tt_and.get_truth_table(),
            self.tt_and.get_variables()
        )

        self.tt_or = TruthTableGenerator("a|b")
        self.calc_or = BooleanDerivativeCalculator(
            self.tt_or.get_truth_table(),
            self.tt_or.get_variables()
        )

        self.tt_xor = TruthTableGenerator("a^b")
        self.calc_xor = BooleanDerivativeCalculator(
            self.tt_xor.get_truth_table(),
            self.tt_xor.get_variables()
        )

        self.tt_three = TruthTableGenerator("a&b|c")
        self.calc_three = BooleanDerivativeCalculator(
            self.tt_three.get_truth_table(),
            self.tt_three.get_variables()
        )

        self.tt_majority = TruthTableGenerator("(a&b)|(a&c)|(b&c)")
        self.calc_majority = BooleanDerivativeCalculator(
            self.tt_majority.get_truth_table(),
            self.tt_majority.get_variables()
        )

    def test_partial_derivative_and_by_a(self):
        derivative = self.calc_and.partial('a')
        self.assertEqual(derivative, 'b')

    def test_partial_derivative_and_by_b(self):
        derivative = self.calc_and.partial('b')
        self.assertEqual(derivative, 'a')

    def test_partial_derivative_or_by_a(self):
        derivative = self.calc_or.partial('a')
        self.assertIsInstance(derivative, str)

    def test_partial_derivative_or_by_b(self):
        derivative = self.calc_or.partial('b')
        self.assertIsInstance(derivative, str)

    def test_partial_derivative_xor_by_a(self):
        derivative = self.calc_xor.partial('a')
        self.assertEqual(derivative, '1')

    def test_partial_derivative_xor_by_b(self):
        derivative = self.calc_xor.partial('b')
        self.assertEqual(derivative, '1')

    def test_partial_table(self):
        table = self.calc_and.partial_table('a')
        self.assertEqual(len(table), 2)
        for comb, val in table:
            self.assertIn(val, [0, 1])

    def test_mixed_table(self):
        table = self.calc_and.mixed_table('a', 'b')
        self.assertEqual(len(table), 1)
        for comb, val in table:
            self.assertIn(val, [0, 1])

    def test_invalid_variable(self):
        with self.assertRaises(ValueError):
            self.calc_and.partial('x')
        with self.assertRaises(ValueError):
            self.calc_and.mixed_table('x', 'y')

    def test_three_variables_partial(self):
        derivative = self.calc_three.partial('a')
        self.assertIsInstance(derivative, str)
        self.assertNotEqual(derivative, "")

    def test_print_partial(self):
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.calc_and.print_partial('a')
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("∂f/∂a", output)

    def test_print_invalid_variable(self):
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.calc_and.print_partial('x')
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("не найдена", output)

    def test_evaluate_with_complex_expression(self):
        result = self.calc_and._evaluate("(a&b)|c", {'a': 1, 'b': 1, 'c': 0})
        self.assertEqual(result, 1)

    def test_evaluate_simple_with_parens(self):
        result = self.calc_and._evaluate_simple("(1 and 0)")
        self.assertEqual(result, 0)

    def test_compute_partial_values(self):
        values = self.calc_and._compute_partial_values('a')
        self.assertEqual(len(values), 2)

    def test_compute_mixed_values(self):
        values = self.calc_and._compute_mixed_values('a', 'b')
        self.assertEqual(len(values), 1)

    def test_to_expression_all_zeros(self):
        result = self.calc_and._to_expression([0, 0, 0, 0], ['a', 'b'])
        self.assertEqual(result, "0")

    def test_to_expression_all_ones(self):
        result = self.calc_and._to_expression([1, 1, 1, 1], ['a', 'b'])
        self.assertEqual(result, "1")

    def test_partial_for_majority(self):
        derivative = self.calc_majority.partial('a')
        self.assertIsInstance(derivative, str)

    def test_partial_derivative_for_constant_function(self):
        truth_table = [
            {'inputs': (0,), 'output': 1},
            {'inputs': (1,), 'output': 1}
        ]
        calc_const = BooleanDerivativeCalculator(truth_table, ['a'])
        derivative = calc_const.partial('a')
        self.assertEqual(derivative, '0')


if __name__ == '__main__':
    unittest.main()
