import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.MinimizationCalculator import MinimizationCalculator
from src.TruthTableGenerator import TruthTableGenerator
from src.NormalFormsBuilder import NormalFormsBuilder


class TestMinimizationCalculator(unittest.TestCase):
    """Тесты для MinimizationCalculator"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.tt_and = TruthTableGenerator("a&b")
        self.builder_and = NormalFormsBuilder(
            self.tt_and.get_truth_table(),
            self.tt_and.get_variables()
        )
        self.sdnf_and, _ = self.builder_and.get_numeric_forms()

        self.tt_or = TruthTableGenerator("a|b")
        self.builder_or = NormalFormsBuilder(
            self.tt_or.get_truth_table(),
            self.tt_or.get_variables()
        )
        self.sdnf_or, _ = self.builder_or.get_numeric_forms()

        self.tt_xor = TruthTableGenerator("a^b")
        self.builder_xor = NormalFormsBuilder(
            self.tt_xor.get_truth_table(),
            self.tt_xor.get_variables()
        )
        self.sdnf_xor, _ = self.builder_xor.get_numeric_forms()

    def test_minimize_and(self):
        """Тест минимизации AND"""
        minimizer = MinimizationCalculator(self.sdnf_and, ['a', 'b'])
        result = minimizer.get_minimized_function()
        self.assertIn("a ∧ b", result)

    def test_minimize_or(self):
        """Тест минимизации OR"""
        minimizer = MinimizationCalculator(self.sdnf_or, ['a', 'b'])
        result = minimizer.get_minimized_function()
        self.assertTrue('a' in result and 'b' in result and '∨' in result)

    def test_minimize_xor(self):
        """Тест минимизации XOR"""
        minimizer = MinimizationCalculator(self.sdnf_xor, ['a', 'b'])
        result = minimizer.get_minimized_function()
        self.assertIn("!a ∧ b", result)
        self.assertIn("a ∧ !b", result)

    def test_term_to_binary(self):
        """Тест преобразования терма в двоичный вид"""
        minimizer = MinimizationCalculator([], ['a', 'b'])
        binary = minimizer._term_to_binary(2)
        self.assertEqual(binary, '10')

    def test_term_to_string_sdnf(self):
        """Тест преобразования терма в строку для СДНФ"""
        minimizer = MinimizationCalculator([], ['a', 'b'])
        term_str = minimizer._term_to_string('10', for_sdnf=True)
        self.assertIn('a', term_str)
        self.assertIn('!b', term_str)

    def test_term_to_string_sknf(self):
        """Тест преобразования терма в строку для СКНФ"""
        minimizer = MinimizationCalculator([], ['a', 'b'])
        term_str = minimizer._term_to_string('10', for_sdnf=False)
        self.assertIn('!a', term_str)
        self.assertIn('b', term_str)

    def test_can_glue(self):
        """Тест возможности склеивания"""
        minimizer = MinimizationCalculator([], ['a', 'b'])
        self.assertTrue(minimizer._can_glue('00', '01'))
        self.assertFalse(minimizer._can_glue('00', '11'))

    def test_glue_terms(self):
        """Тест склеивания термов"""
        minimizer = MinimizationCalculator([], ['a', 'b'])
        result = minimizer._glue_terms('00', '01')
        self.assertEqual(result, '0X')

    def test_covers(self):
        """Тест покрытия"""
        minimizer = MinimizationCalculator([], ['a', 'b'])
        self.assertTrue(minimizer._covers('0X', '00'))
        self.assertFalse(minimizer._covers('0X', '10'))

    def test_empty_sdnf(self):
        """Тест пустой СДНФ"""
        minimizer = MinimizationCalculator([], ['a', 'b'])
        result = minimizer.get_minimized_function()
        self.assertEqual(result, "0")

    def test_print_result(self):
        """Тест вывода результата"""
        import io
        import sys
        minimizer = MinimizationCalculator(self.sdnf_and, ['a', 'b'])
        captured_output = io.StringIO()
        sys.stdout = captured_output
        minimizer.print_result()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Результат", output)


if __name__ == '__main__':
    unittest.main()