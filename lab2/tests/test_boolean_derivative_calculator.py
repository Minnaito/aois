import unittest
from src.BooleanDerivativeCalculator import BooleanDerivativeCalculator
from src.TruthTable import TruthTable
from src.ExpressionParser import BooleanExpressionParser
from src.constants import Constants


class TestBooleanDerivativeCalculator(unittest.TestCase):
    def setUp(self):
        self.parser = BooleanExpressionParser()

    def _create_calculator(self, expr, variables):
        tt = TruthTable(variables, expr, self.parser)
        truth_table_list = [{'inputs': bits, 'output': res} for bits, res in tt]
        return BooleanDerivativeCalculator(truth_table_list, variables)

    def test_partial_derivative_and(self):
        calc = self._create_calculator("a&b", ['a','b'])
        self.assertEqual(calc.partial('a'), 'b')
        self.assertEqual(calc.partial('b'), 'a')

    def test_partial_derivative_xor_like(self):
        calc = self._create_calculator("!(a~b)", ['a','b'])
        self.assertEqual(calc.partial('a'), '1')
        self.assertEqual(calc.partial('b'), '1')

    def test_partial_derivative_constant(self):
        calc = self._create_calculator("1", ['a'])
        self.assertEqual(calc.partial('a'), '0')
        calc = self._create_calculator("0", ['a'])
        self.assertEqual(calc.partial('a'), '0')

    def test_mixed_derivative(self):
        calc = self._create_calculator("a&b&c", ['a','b','c'])
        self.assertEqual(calc.mixed(['a','b']), 'c')
        self.assertEqual(calc.mixed(['a','b','c']), '1')

    def test_mixed_derivative_single_var(self):
        calc = self._create_calculator("a&b", ['a','b'])
        self.assertEqual(calc.mixed(['a']), calc.partial('a'))

    def test_invalid_variable_partial(self):
        calc = self._create_calculator("a", ['a'])
        with self.assertRaises(ValueError):
            calc.partial('x')

    def test_invalid_variable_mixed(self):
        calc = self._create_calculator("a", ['a'])
        with self.assertRaises(ValueError):
            calc.mixed(['x'])

    def test_duplicate_variables_mixed(self):
        calc = self._create_calculator("a&b", ['a','b'])
        with self.assertRaises(ValueError):
            calc.mixed(['a','a'])

    def test_print_all(self):
        calc = self._create_calculator("a&b", ['a','b'])
        calc.print_all(max_order=2)

    def test_expression_as_string_initialization(self):
        calc = BooleanDerivativeCalculator("a&b", ['a','b'])
        self.assertEqual(calc.partial('a'), 'b')

    def test_convert_table_to_dict(self):
        table = [{'inputs': (0,0), 'output': 0}, {'inputs': (0,1), 'output': 0},
                 {'inputs': (1,0), 'output': 0}, {'inputs': (1,1), 'output': 1}]
        calc = BooleanDerivativeCalculator(table, ['a','b'])
        self.assertEqual(calc.partial('a'), 'b')

    def test_evaluate_with_implication(self):
        calc = self._create_calculator("a->b", ['a','b'])
        self.assertEqual(calc.partial('a'), '¬b')
        self.assertEqual(calc.partial('b'), 'a')

    def test_evaluate_with_equivalence(self):
        calc = self._create_calculator("a~b", ['a','b'])
        self.assertEqual(calc.partial('a'), '1')
        self.assertEqual(calc.partial('b'), '1')

    def test_mixed_derivative_four_vars(self):
        calc = self._create_calculator("a&b&c&d", ['a','b','c','d'])
        self.assertEqual(calc.mixed(['a','b','c','d']), '1')

    def test_to_expression_all_zeros(self):
        calc = BooleanDerivativeCalculator("0", ['a'])
        expr = calc._to_expression([0,0], ['a'])
        self.assertEqual(expr, "0")

    def test_to_expression_all_ones(self):
        calc = BooleanDerivativeCalculator("1", ['a'])
        expr = calc._to_expression([1,1], ['a'])
        self.assertEqual(expr, "1")

    def test_simplify_method_exists(self):
        calc = BooleanDerivativeCalculator("a", ['a','b'])
        try:
            result = calc._simplify("a ∨ b", ['a','b'])
        except Exception as e:
            self.fail(f"_simplify raised exception: {e}")

    def test_evaluate_simple_not(self):
        calc = BooleanDerivativeCalculator("!a", ['a'])
        result = calc._evaluate_simple("not 1")
        self.assertEqual(result, 0)
        result = calc._evaluate_simple("not 0")
        self.assertEqual(result, 1)

    def test_evaluate_simple_and(self):
        calc = BooleanDerivativeCalculator("a", ['a'])
        result = calc._evaluate_simple("1 and 1")
        self.assertEqual(result, 1)
        result = calc._evaluate_simple("1 and 0")
        self.assertEqual(result, 0)

    def test_evaluate_simple_or(self):
        calc = BooleanDerivativeCalculator("a", ['a'])
        result = calc._evaluate_simple("1 or 0")
        self.assertEqual(result, 1)
        result = calc._evaluate_simple("0 or 0")
        self.assertEqual(result, 0)

    def test_evaluate_simple_equiv(self):
        calc = BooleanDerivativeCalculator("a", ['a'])
        result = calc._evaluate_simple("1 == 1")
        self.assertEqual(result, 1)
        result = calc._evaluate_simple("1 == 0")
        self.assertEqual(result, 0)

    def test_evaluate_with_invalid_expr(self):
        calc = BooleanDerivativeCalculator("a", ['a'])
        result = calc._evaluate("invalid", {'a': 1})
        self.assertEqual(result, 0)

    def test_partial_derivative_complex(self):
        calc = self._create_calculator("a|b", ['a','b'])
        self.assertEqual(calc.partial('a'), '¬b')
        self.assertEqual(calc.partial('b'), '¬a')

    def test_mixed_derivative_order_three(self):
        calc = self._create_calculator("a&b&c", ['a','b','c'])
        result = calc.mixed(['a','b','c'])
        self.assertEqual(result, '1')

    def test_mixed_derivative_duplicate_variables(self):
        """Тест смешанной производной с дублирующимися переменными"""
        calc = BooleanDerivativeCalculator("a&b", ['a', 'b'])
        with self.assertRaises(ValueError):
            calc.mixed(['a', 'a'])

    def test_mixed_derivative_variable_not_found(self):
        """Тест смешанной производной с несуществующей переменной"""
        calc = BooleanDerivativeCalculator("a&b", ['a', 'b'])
        with self.assertRaises(ValueError):
            calc.mixed(['a', 'c'])


if __name__ == '__main__':
    unittest.main()
