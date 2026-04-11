import unittest
from src.DummyVariableFinder import DummyVariableFinder
from src.TruthTable import TruthTable
from src.ExpressionParser import BooleanExpressionParser


class TestDummyVariableFinder(unittest.TestCase):
    def setUp(self):
        self.parser = BooleanExpressionParser()

    def _find_dummies(self, expr, variables):
        tt = TruthTable(variables, expr, self.parser)
        truth_table_list = [{'inputs': bits, 'output': res} for bits, res in tt]
        return DummyVariableFinder(truth_table_list, variables)

    def test_no_dummy_variables(self):
        finder = self._find_dummies("a&b", ['a','b'])
        self.assertEqual(finder.get_dummy_variables(), [])

    def test_dummy_variable_present(self):
        finder = self._find_dummies("a&b", ['a','b','c'])
        self.assertEqual(finder.get_dummy_variables(), ['c'])

    def test_multiple_dummy_variables(self):
        finder = self._find_dummies("1", ['a','b'])
        self.assertEqual(set(finder.get_dummy_variables()), {'a','b'})

    def test_print_results(self):
        finder = self._find_dummies("a&b", ['a','b','c'])
        finder.print_results()  # smoke test

    def test_is_dummy_with_invalid_input_length(self):
        """Тест _is_dummy с некорректной длиной inputs"""
        truth_table = [
            {'inputs': (0,), 'output': 0},  # Неправильная длина
            {'inputs': (0, 0), 'output': 0},
            {'inputs': (0, 1), 'output': 0},
            {'inputs': (1, 0), 'output': 0},
            {'inputs': (1, 1), 'output': 0}
        ]
        finder = DummyVariableFinder(truth_table, ['a', 'b'])
        # Должно обработаться без ошибок
        self.assertIsNotNone(finder.get_dummy_variables())


if __name__ == '__main__':
    unittest.main()
