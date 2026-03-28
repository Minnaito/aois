import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.TruthTableGenerator import TruthTableGenerator


class TestTruthTableGenerator(unittest.TestCase):
    """Тесты для TruthTableGenerator"""

    def test_extract_variables_simple(self):
        tt = TruthTableGenerator("a&b")
        self.assertEqual(set(tt.get_variables()), {'a', 'b'})

    def test_extract_variables_complex(self):
        tt = TruthTableGenerator("(a|b)&!c")
        self.assertEqual(set(tt.get_variables()), {'a', 'b', 'c'})

    def test_extract_variables_with_impl(self):
        tt = TruthTableGenerator("a->b")
        self.assertEqual(set(tt.get_variables()), {'a', 'b'})

    def test_constant_function(self):
        tt = TruthTableGenerator("1")
        self.assertEqual(tt.get_variables(), [])
        table = tt.get_truth_table()
        self.assertEqual(len(table), 1)

    def test_and_function(self):
        tt = TruthTableGenerator("a&b")
        table = tt.get_truth_table()
        values = {row['inputs']: row['output'] for row in table}
        self.assertEqual(values[(0, 0)], 0)
        self.assertEqual(values[(0, 1)], 0)
        self.assertEqual(values[(1, 0)], 0)
        self.assertEqual(values[(1, 1)], 1)

    def test_or_function(self):
        tt = TruthTableGenerator("a|b")
        table = tt.get_truth_table()
        values = {row['inputs']: row['output'] for row in table}
        self.assertEqual(values[(0, 0)], 0)
        self.assertEqual(values[(0, 1)], 1)
        self.assertEqual(values[(1, 0)], 1)
        self.assertEqual(values[(1, 1)], 1)

    def test_not_function(self):
        tt = TruthTableGenerator("!a")
        table = tt.get_truth_table()
        values = {row['inputs']: row['output'] for row in table}
        self.assertEqual(values[(0,)], 1)
        self.assertEqual(values[(1,)], 0)

    def test_xor_function(self):
        tt = TruthTableGenerator("a^b")
        table = tt.get_truth_table()
        values = {row['inputs']: row['output'] for row in table}
        self.assertEqual(values[(0, 0)], 0)
        self.assertEqual(values[(0, 1)], 1)
        self.assertEqual(values[(1, 0)], 1)
        self.assertEqual(values[(1, 1)], 0)

    def test_implication_function(self):
        tt = TruthTableGenerator("a->b")
        table = tt.get_truth_table()
        values = {row['inputs']: row['output'] for row in table}
        self.assertEqual(values[(0, 0)], 1)
        self.assertEqual(values[(0, 1)], 1)
        self.assertEqual(values[(1, 0)], 0)
        self.assertEqual(values[(1, 1)], 1)

    def test_equivalence_function(self):
        tt = TruthTableGenerator("a~b")
        table = tt.get_truth_table()
        values = {row['inputs']: row['output'] for row in table}
        self.assertEqual(values[(0, 0)], 1)
        self.assertEqual(values[(0, 1)], 0)
        self.assertEqual(values[(1, 0)], 0)
        self.assertEqual(values[(1, 1)], 1)

    def test_complex_expression(self):
        tt = TruthTableGenerator("(a&b)|(!c)")
        table = tt.get_truth_table()
        self.assertEqual(len(table), 8)

    def test_get_function_values(self):
        tt = TruthTableGenerator("a&b")
        values = tt.get_function_values()
        self.assertEqual(len(values), 4)

    def test_parse_expression_with_complex_implication_multiple(self):
        """Тест парсинга с множественными импликациями"""
        tt = TruthTableGenerator("a->b->c")
        result = tt._parse_expression("a->b->c", {'a': 1, 'b': 1, 'c': 0})
        self.assertIn(result, [True, False])

    def test_safe_evaluate_simple_and(self):
        """Тест безопасного вычисления AND"""
        tt = TruthTableGenerator("a&b")
        result = tt._safe_evaluate("1 and 1")
        self.assertTrue(result)

    def test_safe_evaluate_simple_or(self):
        """Тест безопасного вычисления OR"""
        tt = TruthTableGenerator("a|b")
        result = tt._safe_evaluate("0 or 0")
        self.assertFalse(result)

    def test_safe_evaluate_not(self):
        """Тест безопасного вычисления NOT"""
        tt = TruthTableGenerator("!a")
        result = tt._safe_evaluate("not 0")
        self.assertTrue(result)

    def test_safe_evaluate_xor(self):
        """Тест безопасного вычисления XOR"""
        tt = TruthTableGenerator("a^b")
        result = tt._safe_evaluate("1 != 0")
        self.assertTrue(result)

    def test_safe_evaluate_equiv(self):
        """Тест безопасного вычисления эквивалентности"""
        tt = TruthTableGenerator("a~b")
        result = tt._safe_evaluate("1 == 1")
        self.assertTrue(result)

    def test_safe_evaluate_with_parens(self):
        """Тест безопасного вычисления со скобками"""
        tt = TruthTableGenerator("a&b")
        result = tt._safe_evaluate("(1 and 0)")
        self.assertFalse(result)

    def test_safe_evaluate_number(self):
        """Тест безопасного вычисления числа"""
        tt = TruthTableGenerator("1")
        result = tt._safe_evaluate("1")
        self.assertTrue(result)

    def test_safe_evaluate_zero(self):
        """Тест безопасного вычисления нуля"""
        tt = TruthTableGenerator("0")
        result = tt._safe_evaluate("0")
        self.assertFalse(result)

    def test_safe_evaluate_invalid(self):
        """Тест безопасного вычисления некорректного выражения"""
        tt = TruthTableGenerator("a&b")
        result = tt._safe_evaluate("invalid")
        self.assertFalse(result)

    def test_empty_truth_table_print(self):
        """Тест вывода пустой таблицы"""
        tt = TruthTableGenerator("a&b")
        tt.truth_table = []
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        tt.print_truth_table()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Таблица истинности пуста", output)

    def test_print_truth_table_constant(self):
        """Тест вывода константной функции"""
        tt = TruthTableGenerator("1")
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        tt.print_truth_table()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Константная функция", output)


if __name__ == '__main__':
    unittest.main()