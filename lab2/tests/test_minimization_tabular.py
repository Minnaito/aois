import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.MinimizationTabular import MinimizationTabular
from src.TruthTableGenerator import TruthTableGenerator
from src.NormalFormsBuilder import NormalFormsBuilder


class TestMinimizationTabular(unittest.TestCase):
    """Тесты для MinimizationTabular"""

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

    def test_minimize_and(self):
        """Тест минимизации AND"""
        minimizer = MinimizationTabular(self.sdnf_and, ['a', 'b'])
        result = minimizer.get_minimized_function()
        # Проверяем, что результат содержит a и b
        self.assertTrue('a' in result and 'b' in result)

    def test_minimize_or(self):
        """Тест минимизации OR"""
        minimizer = MinimizationTabular(self.sdnf_or, ['a', 'b'])
        result = minimizer.get_minimized_function()
        self.assertTrue('a' in result and 'b' in result)

    def test_term_to_binary(self):
        """Тест преобразования терма в двоичный вид"""
        minimizer = MinimizationTabular([], ['a', 'b'])
        binary = minimizer._term_to_binary(2)
        self.assertEqual(binary, '10')

    def test_can_glue(self):
        """Тест возможности склеивания"""
        minimizer = MinimizationTabular([], ['a', 'b'])
        self.assertTrue(minimizer._can_glue('00', '01'))
        self.assertFalse(minimizer._can_glue('00', '11'))

    def test_glue_terms(self):
        """Тест склеивания термов"""
        minimizer = MinimizationTabular([], ['a', 'b'])
        result = minimizer._glue_terms('00', '01')
        self.assertEqual(result, '0X')

    def test_get_implicant_string(self):
        """Тест преобразования импликанты в строку"""
        minimizer = MinimizationTabular([], ['a', 'b'])
        imp_str = minimizer._get_implicant_string('0X')
        self.assertIn('!a', imp_str)

    def test_covers(self):
        """Тест покрытия"""
        minimizer = MinimizationTabular([], ['a', 'b'])
        self.assertTrue(minimizer._covers('0X', '00'))
        self.assertFalse(minimizer._covers('0X', '10'))

    def test_build_implicants(self):
        """Тест построения импликант"""
        minimizer = MinimizationTabular(self.sdnf_and, ['a', 'b'])
        minimizer._build_implicants()
        self.assertIsNotNone(minimizer.implicants)

    def test_build_table(self):
        """Тест построения таблицы"""
        minimizer = MinimizationTabular(self.sdnf_and, ['a', 'b'])
        minimizer._build_implicants()
        minimizer._build_table()
        self.assertIsNotNone(minimizer.table)

    def test_find_essential_implicants(self):
        """Тест поиска существенных импликант"""
        minimizer = MinimizationTabular(self.sdnf_and, ['a', 'b'])
        minimizer._build_implicants()
        minimizer._build_table()
        essential = minimizer._find_essential_implicants()
        self.assertIsNotNone(essential)

    def test_empty_sdnf(self):
        """Тест пустой СДНФ"""
        minimizer = MinimizationTabular([], ['a', 'b'])
        result = minimizer.get_minimized_function()
        self.assertEqual(result, "0")

    def test_print_table(self):
        """Тест вывода таблицы"""
        import io
        import sys
        minimizer = MinimizationTabular(self.sdnf_and, ['a', 'b'])
        minimizer._build_implicants()
        minimizer._build_table()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        minimizer.print_table()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("ТАБЛИЦА ПОКРЫТИЙ", output)

    def test_print_result(self):
        """Тест вывода результата"""
        import io
        import sys
        minimizer = MinimizationTabular(self.sdnf_and, ['a', 'b'])
        captured_output = io.StringIO()
        sys.stdout = captured_output
        minimizer.print_result()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Результат минимизации", output)


if __name__ == '__main__':
    unittest.main()