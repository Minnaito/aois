import unittest
from src.NormalFormsBuilder import NormalFormsBuilder
from src.TruthTable import TruthTable
from src.ExpressionParser import BooleanExpressionParser


class TestNormalFormsBuilder(unittest.TestCase):
    def setUp(self):
        self.parser = BooleanExpressionParser()

    def _build_from_expression(self, expr, variables):
        tt = TruthTable(variables, expr, self.parser)
        truth_table_list = [{'inputs': bits, 'output': res} for bits, res in tt]
        return NormalFormsBuilder(truth_table_list, variables)

    def test_build_sknf_term_without_variables(self):
        """Тест построения СКНФ терма без переменных"""
        builder = NormalFormsBuilder([{'inputs': (), 'output': 0}], [])
        term = builder._build_sknf_term(())
        self.assertEqual(term, "0")

    def test_sdnf_sknf_simple_and(self):
        nf = self._build_from_expression("a&b", ['a','b'])
        self.assertEqual(nf.get_sdnf(), "(a ∧ b)")
        self.assertEqual(nf.get_sknf(), "(a ∨ b) ∧ (a ∨ !b) ∧ (!a ∨ b)")
        self.assertEqual(nf.get_numeric_forms(), ([3], [0,1,2]))

    def test_sdnf_sknf_constant_one(self):
        nf = self._build_from_expression("1", [])
        self.assertEqual(nf.get_sdnf(), "1")
        self.assertEqual(nf.get_sknf(), "1")
        self.assertEqual(nf.get_numeric_forms(), ([0], []))

    def test_sdnf_sknf_constant_zero(self):
        nf = self._build_from_expression("0", [])
        self.assertEqual(nf.get_sdnf(), "0")
        self.assertEqual(nf.get_sknf(), "0")
        self.assertEqual(nf.get_numeric_forms(), ([], [0]))

    def test_index_form(self):
        nf = self._build_from_expression("a|b", ['a','b'])
        self.assertEqual(nf.get_index_form(), "0111")

    def test_print_forms(self):
        nf = self._build_from_expression("a", ['a'])
        nf.print_forms()

    def test_single_variable_constant(self):
        nf = self._build_from_expression("a", ['a'])
        self.assertEqual(nf.get_sdnf(), "a")
        self.assertEqual(nf.get_sknf(), "a")

    def test_get_inputs_from_index(self):
        from src.NormalFormsBuilder import NormalFormsBuilder
        nf = NormalFormsBuilder([], ['a','b','c'])
        inputs = nf._get_inputs_from_index(5, 3)
        self.assertEqual(inputs, (1, 0, 1))


if __name__ == '__main__':
    unittest.main()
