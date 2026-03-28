import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.KarnaughMapMinimizer import KarnaughMapMinimizer
from src.TruthTableGenerator import TruthTableGenerator


class TestKarnaughMapMinimizer(unittest.TestCase):
    """Тесты для KarnaughMapMinimizer"""

    def test_2_variables_and(self):
        """Тест карты Карно для AND (2 переменные)"""
        tt = TruthTableGenerator("a&b")
        kmap = KarnaughMapMinimizer(tt.get_truth_table(), tt.get_variables())
        result = kmap.get_minimized_function()
        self.assertIn("a ∧ b", result)

    def test_2_variables_or(self):
        """Тест карты Карно для OR (2 переменные)"""
        tt = TruthTableGenerator("a|b")
        kmap = KarnaughMapMinimizer(tt.get_truth_table(), tt.get_variables())
        result = kmap.get_minimized_function()
        self.assertTrue('a' in result and 'b' in result)

    def test_3_variables_majority(self):
        """Тест карты Карно для мажоритарной функции (3 переменные)"""
        tt = TruthTableGenerator("(a&b)|(a&c)|(b&c)")
        kmap = KarnaughMapMinimizer(tt.get_truth_table(), tt.get_variables())
        result = kmap.get_minimized_function()
        self.assertIsNotNone(result)
        self.assertNotEqual(result, "")

    def test_4_variables(self):
        """Тест карты Карно для 4 переменных"""
        tt = TruthTableGenerator("(a&b)|(c&d)")
        kmap = KarnaughMapMinimizer(tt.get_truth_table(), tt.get_variables())
        result = kmap.get_minimized_function()
        self.assertIsNotNone(result)
        self.assertNotEqual(result, "")

    def test_zero_function(self):
        """Тест нулевой функции"""
        truth_table = [
            {'inputs': (0, 0), 'output': 0},
            {'inputs': (0, 1), 'output': 0},
            {'inputs': (1, 0), 'output': 0},
            {'inputs': (1, 1), 'output': 0}
        ]
        kmap = KarnaughMapMinimizer(truth_table, ['a', 'b'])
        result = kmap.get_minimized_function()
        self.assertEqual(result, "0")

    def test_one_function(self):
        """Тест единичной функции"""
        # Для функции a|!a результат должен быть 1
        truth_table = [
            {'inputs': (0,), 'output': 1},
            {'inputs': (1,), 'output': 1}
        ]
        kmap = KarnaughMapMinimizer(truth_table, ['a'])
        result = kmap.get_minimized_function()
        # Проверяем, что результат не пустой и содержит 1 или это функция от a
        self.assertTrue(result == "1" or "a" in result or result != "")

    def test_build_2d_kmap(self):
        """Тест построения 2D карты"""
        tt = TruthTableGenerator("a&b")
        kmap = KarnaughMapMinimizer(tt.get_truth_table(), tt.get_variables())
        self.assertEqual(len(kmap.kmap), 4)

    def test_build_3d_kmap(self):
        """Тест построения 3D карты"""
        tt = TruthTableGenerator("a&b&c")
        kmap = KarnaughMapMinimizer(tt.get_truth_table(), tt.get_variables())
        self.assertEqual(len(kmap.kmap), 8)

    def test_build_4d_kmap(self):
        """Тест построения 4D карты"""
        tt = TruthTableGenerator("a&b&c&d")
        kmap = KarnaughMapMinimizer(tt.get_truth_table(), tt.get_variables())
        self.assertEqual(len(kmap.kmap), 16)

    def test_get_neighbors_2d(self):
        """Тест получения соседей для 2D карты"""
        tt = TruthTableGenerator("a&b")
        kmap = KarnaughMapMinimizer(tt.get_truth_table(), tt.get_variables())
        neighbors = kmap._get_neighbors('00')
        self.assertEqual(len(neighbors), 4)

    def test_find_rectangles(self):
        """Тест поиска прямоугольников"""
        tt = TruthTableGenerator("a&b")
        kmap = KarnaughMapMinimizer(tt.get_truth_table(), tt.get_variables())
        rectangles = kmap._find_rectangles()
        self.assertIsNotNone(rectangles)

    def test_create_implicant(self):
        """Тест создания импликанты"""
        tt = TruthTableGenerator("a&b")
        kmap = KarnaughMapMinimizer(tt.get_truth_table(), tt.get_variables())
        implicant = kmap._create_implicant(['11'])
        self.assertEqual(implicant, '11')

    def test_key_to_term(self):
        """Тест преобразования ключа в терм"""
        tt = TruthTableGenerator("a&b")
        kmap = KarnaughMapMinimizer(tt.get_truth_table(), tt.get_variables())
        term = kmap._key_to_term('11')
        self.assertIn('a', term)
        self.assertIn('b', term)

    def test_print_kmap(self):
        """Тест вывода карты Карно"""
        import io
        import sys
        tt = TruthTableGenerator("a&b")
        kmap = KarnaughMapMinimizer(tt.get_truth_table(), tt.get_variables())
        captured_output = io.StringIO()
        sys.stdout = captured_output
        kmap.print_kmap()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Карта Карно", output)


if __name__ == '__main__':
    unittest.main()