import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.NormalFormsBuilder import NormalFormsBuilder
from src.TruthTableGenerator import TruthTableGenerator


class TestNormalFormsBuilder(unittest.TestCase):
    """Тесты для NormalFormsBuilder"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.tt_and = TruthTableGenerator("a&b")
        self.builder_and = NormalFormsBuilder(
            self.tt_and.get_truth_table(),
            self.tt_and.get_variables()
        )

        self.tt_or = TruthTableGenerator("a|b")
        self.builder_or = NormalFormsBuilder(
            self.tt_or.get_truth_table(),
            self.tt_or.get_variables()
        )

        self.tt_xor = TruthTableGenerator("a^b")
        self.builder_xor = NormalFormsBuilder(
            self.tt_xor.get_truth_table(),
            self.tt_xor.get_variables()
        )

    def test_sdnf_and(self):
        """Тест СДНФ для AND"""
        sdnf = self.builder_and.get_sdnf()
        self.assertIn("(a ∧ b)", sdnf)

    def test_sknf_and(self):
        """Тест СКНФ для AND"""
        sknf = self.builder_and.get_sknf()
        self.assertIn("(a ∨ b)", sknf)

    def test_numeric_forms_and(self):
        """Тест числовых форм для AND"""
        sdnf_terms, sknf_terms = self.builder_and.get_numeric_forms()
        self.assertEqual(sdnf_terms, [3])
        self.assertEqual(sknf_terms, [0, 1, 2])

    def test_sdnf_or(self):
        """Тест СДНФ для OR"""
        sdnf = self.builder_or.get_sdnf()
        self.assertIn("(!a ∧ b)", sdnf)
        self.assertIn("(a ∧ !b)", sdnf)
        self.assertIn("(a ∧ b)", sdnf)

    def test_sknf_or(self):
        """Тест СКНФ для OR"""
        sknf = self.builder_or.get_sknf()
        self.assertIn("(a ∨ b)", sknf)

    def test_numeric_forms_or(self):
        """Тест числовых форм для OR"""
        sdnf_terms, sknf_terms = self.builder_or.get_numeric_forms()
        self.assertEqual(sdnf_terms, [1, 2, 3])
        self.assertEqual(sknf_terms, [0])

    def test_sdnf_xor(self):
        """Тест СДНФ для XOR"""
        sdnf = self.builder_xor.get_sdnf()
        self.assertIn("(!a ∧ b)", sdnf)
        self.assertIn("(a ∧ !b)", sdnf)

    def test_sknf_xor(self):
        """Тест СКНФ для XOR"""
        sknf = self.builder_xor.get_sknf()
        self.assertIn("(a ∨ b)", sknf)
        self.assertIn("(!a ∨ !b)", sknf)

    def test_index_form(self):
        """Тест индексной формы"""
        index_form = self.builder_and.get_index_form()
        # AND: a&b дает 0001 = 1
        self.assertIn("0001 (1)", index_form)

    def test_zero_function(self):
        """Тест нулевой функции"""
        tt_zero = TruthTableGenerator("a&!a")
        builder_zero = NormalFormsBuilder(
            tt_zero.get_truth_table(),
            tt_zero.get_variables()
        )
        self.assertEqual(builder_zero.get_sdnf(), "0")

    def test_one_function(self):
        """Тест единичной функции"""
        tt_one = TruthTableGenerator("a|!a")
        builder_one = NormalFormsBuilder(
            tt_one.get_truth_table(),
            tt_one.get_variables()
        )
        self.assertEqual(builder_one.get_sknf(), "1")


if __name__ == '__main__':
    unittest.main()