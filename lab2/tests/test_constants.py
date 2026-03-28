import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants import Constants


class TestConstants(unittest.TestCase):
    """Тесты для класса Constants"""

    def test_numeric_constants(self):
        """Тест числовых констант"""
        self.assertEqual(Constants.ZERO, 0)
        self.assertEqual(Constants.ONE, 1)
        self.assertEqual(Constants.TWO, 2)
        self.assertEqual(Constants.THREE, 3)
        self.assertEqual(Constants.FOUR, 4)
        self.assertEqual(Constants.FIVE, 5)

    def test_index_constants(self):
        """Тест индексных констант"""
        self.assertEqual(Constants.ZERO_INDEX, 0)
        self.assertEqual(Constants.FIRST_INDEX, 1)
        self.assertEqual(Constants.SECOND_INDEX, 2)
        self.assertEqual(Constants.THIRD_INDEX, 3)
        self.assertEqual(Constants.FOURTH_INDEX, 4)

    def test_os_constants(self):
        """Тест констант ОС"""
        self.assertEqual(Constants.OS_WINDOWS, 'nt')
        self.assertEqual(Constants.CLEAR_CMD_WINDOWS, 'cls')
        self.assertEqual(Constants.CLEAR_CMD_UNIX, 'clear')

    def test_variables(self):
        """Тест списка переменных"""
        self.assertEqual(Constants.VARIABLES, ['a', 'b', 'c', 'd', 'e'])
        self.assertEqual(Constants.get_variables_up_to(3), ['a', 'b', 'c'])
        self.assertEqual(Constants.get_variables_up_to(5), ['a', 'b', 'c', 'd', 'e'])

    def test_post_classes(self):
        """Тест классов Поста"""
        self.assertEqual(Constants.CLASS_T0, "T0")
        self.assertEqual(Constants.CLASS_T1, "T1")
        self.assertEqual(Constants.CLASS_S, "S")
        self.assertEqual(Constants.CLASS_M, "M")
        self.assertEqual(Constants.CLASS_L, "L")

    def test_operations(self):
        """Тест операций"""
        self.assertEqual(Constants.OP_NOT, '!')
        self.assertEqual(Constants.OP_AND, '&')
        self.assertEqual(Constants.OP_OR, '|')
        self.assertEqual(Constants.OP_XOR, '^')
        self.assertEqual(Constants.OP_IMPL, '->')
        self.assertEqual(Constants.OP_EQUIV, '~')

    def test_format_error(self):
        """Тест форматирования ошибок"""
        error = Constants.format_error(Constants.ERROR_VARIABLE_NOT_FOUND, var='x')
        self.assertEqual(error, "Переменная 'x' не найдена")

    def test_get_kmap_order(self):
        """Тест получения порядка карты Карно"""
        self.assertEqual(Constants.get_kmap_order(2), Constants.KMAP_ORDER_2)
        self.assertEqual(Constants.get_kmap_order(3), Constants.KMAP_ORDER_2)
        self.assertEqual(Constants.get_kmap_order(5), Constants.KMAP_ORDER_4)

    def test_get_rect_sizes(self):
        """Тест получения размеров прямоугольников"""
        self.assertEqual(Constants.get_rect_sizes(2), Constants.KMAP_RECT_SIZES_2)
        self.assertEqual(Constants.get_rect_sizes(3), Constants.KMAP_RECT_SIZES_3)
        self.assertEqual(Constants.get_rect_sizes(4), Constants.KMAP_RECT_SIZES_4)
        self.assertEqual(Constants.get_rect_sizes(5), Constants.KMAP_RECT_SIZES_5)


if __name__ == '__main__':
    unittest.main()