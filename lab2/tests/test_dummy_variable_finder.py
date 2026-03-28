import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.DummyVariableFinder import DummyVariableFinder
from src.TruthTableGenerator import TruthTableGenerator


class TestDummyVariableFinder(unittest.TestCase):
    """Тесты для DummyVariableFinder"""

    def test_no_dummy_variables_and(self):
        """Тест AND - нет фиктивных переменных"""
        tt = TruthTableGenerator("a&b")
        finder = DummyVariableFinder(tt.get_truth_table(), tt.get_variables())
        dummy_vars = finder.get_dummy_variables()
        self.assertEqual(dummy_vars, [])

    def test_dummy_variable_or_with_duplicate(self):
        """Тест OR с дублированием"""
        truth_table = [
            {'inputs': (0, 0), 'output': 0},
            {'inputs': (0, 1), 'output': 0},
            {'inputs': (1, 0), 'output': 1},
            {'inputs': (1, 1), 'output': 1}
        ]
        finder = DummyVariableFinder(truth_table, ['a', 'b'])
        dummy_vars = finder.get_dummy_variables()
        self.assertIn('b', dummy_vars)

    def test_all_dummy_variables(self):
        """Тест все переменные фиктивные"""
        truth_table = [
            {'inputs': (0, 0), 'output': 1},
            {'inputs': (0, 1), 'output': 1},
            {'inputs': (1, 0), 'output': 1},
            {'inputs': (1, 1), 'output': 1}
        ]
        finder = DummyVariableFinder(truth_table, ['a', 'b'])
        dummy_vars = finder.get_dummy_variables()
        self.assertEqual(set(dummy_vars), {'a', 'b'})

    def test_one_dummy_variable(self):
        """Тест одна фиктивная переменная"""
        truth_table = [
            {'inputs': (0, 0), 'output': 0},
            {'inputs': (0, 1), 'output': 0},
            {'inputs': (1, 0), 'output': 1},
            {'inputs': (1, 1), 'output': 1}
        ]
        finder = DummyVariableFinder(truth_table, ['a', 'b'])
        dummy_vars = finder.get_dummy_variables()
        self.assertEqual(dummy_vars, ['b'])

    def test_no_dummy_variables_xor(self):
        """Тест XOR - нет фиктивных переменных"""
        tt = TruthTableGenerator("a^b")
        finder = DummyVariableFinder(tt.get_truth_table(), tt.get_variables())
        dummy_vars = finder.get_dummy_variables()
        self.assertEqual(dummy_vars, [])

    def test_is_dummy_method(self):
        """Тест внутреннего метода _is_dummy"""
        truth_table = [
            {'inputs': (0, 0), 'output': 0},
            {'inputs': (0, 1), 'output': 0},
            {'inputs': (1, 0), 'output': 1},
            {'inputs': (1, 1), 'output': 1}
        ]
        finder = DummyVariableFinder(truth_table, ['a', 'b'])
        self.assertTrue(finder._is_dummy(1))
        self.assertFalse(finder._is_dummy(0))

    def test_get_dummy_variables(self):
        """Тест получения фиктивных переменных"""
        truth_table = [
            {'inputs': (0, 0), 'output': 0},
            {'inputs': (0, 1), 'output': 0},
            {'inputs': (1, 0), 'output': 1},
            {'inputs': (1, 1), 'output': 1}
        ]
        finder = DummyVariableFinder(truth_table, ['a', 'b'])
        dummy_vars = finder.get_dummy_variables()
        self.assertEqual(dummy_vars, ['b'])

    def test_dummy_variable_with_three_vars(self):
        """Тест с тремя переменными"""
        truth_table = [
            {'inputs': (0, 0, 0), 'output': 0},
            {'inputs': (0, 0, 1), 'output': 0},
            {'inputs': (0, 1, 0), 'output': 0},
            {'inputs': (0, 1, 1), 'output': 0},
            {'inputs': (1, 0, 0), 'output': 1},
            {'inputs': (1, 0, 1), 'output': 1},
            {'inputs': (1, 1, 0), 'output': 1},
            {'inputs': (1, 1, 1), 'output': 1}
        ]
        finder = DummyVariableFinder(truth_table, ['a', 'b', 'c'])
        dummy_vars = finder.get_dummy_variables()
        self.assertEqual(set(dummy_vars), {'b', 'c'})

    def test_dummy_variable_print_no_dummy(self):
        """Тест вывода когда нет фиктивных переменных"""
        truth_table = [
            {'inputs': (0, 0), 'output': 0},
            {'inputs': (0, 1), 'output': 0},
            {'inputs': (1, 0), 'output': 0},
            {'inputs': (1, 1), 'output': 1}
        ]
        finder = DummyVariableFinder(truth_table, ['a', 'b'])
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        finder.print_results()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Фиктивные переменные не обнаружены", output)


if __name__ == '__main__':
    unittest.main()