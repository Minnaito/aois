import unittest
from src.constants import Constants


class TestConstants(unittest.TestCase):
    def test_numeric_constants(self):
        self.assertEqual(Constants.ZERO, 0)
        self.assertEqual(Constants.ONE, 1)
        self.assertEqual(Constants.TWO, 2)
        self.assertEqual(Constants.THREE, 3)
        self.assertEqual(Constants.FOUR, 4)
        self.assertEqual(Constants.FIVE, 5)

    def test_get_rect_sizes_five(self):
        """Тест получения размеров прямоугольников для 5 переменных"""
        sizes = Constants.get_rect_sizes(5)
        self.assertEqual(sizes, Constants.KMAP_RECT_SIZES_5)

    def test_index_constants(self):
        self.assertEqual(Constants.ZERO_INDEX, 0)
        self.assertEqual(Constants.FIRST_INDEX, 1)
        self.assertEqual(Constants.SECOND_INDEX, 2)
        self.assertEqual(Constants.THIRD_INDEX, 3)
        self.assertEqual(Constants.FOURTH_INDEX, 4)

    def test_os_constants(self):
        self.assertEqual(Constants.OS_WINDOWS, 'nt')
        self.assertEqual(Constants.CLEAR_CMD_WINDOWS, 'cls')
        self.assertEqual(Constants.CLEAR_CMD_UNIX, 'clear')

    def test_exit_code(self):
        self.assertEqual(Constants.EXIT_SUCCESS, 0)

    def test_max_variables(self):
        self.assertEqual(Constants.MAX_VARIABLES, 5)

    def test_variables_list(self):
        self.assertEqual(Constants.VARIABLES, ['a', 'b', 'c', 'd', 'e'])

    def test_post_classes(self):
        self.assertEqual(Constants.CLASS_T0, "T0")
        self.assertEqual(Constants.CLASS_T1, "T1")
        self.assertEqual(Constants.CLASS_S, "S")
        self.assertEqual(Constants.CLASS_M, "M")
        self.assertEqual(Constants.CLASS_L, "L")

    def test_derivative_types(self):
        self.assertEqual(Constants.DERIVATIVE_SIMPLE, "simple")
        self.assertEqual(Constants.DERIVATIVE_MIXED, "mixed")

    def test_kmap_orders(self):
        self.assertEqual(Constants.KMAP_ORDER_2, ['00', '01', '11', '10'])
        self.assertEqual(Constants.KMAP_ORDER_3, ['00', '01', '11', '10'])
        self.assertEqual(Constants.KMAP_ORDER_4, ['00', '01', '11', '10'])

    def test_rect_sizes(self):
        self.assertIn((2, 2), Constants.KMAP_RECT_SIZES_2)
        self.assertIn((4, 2), Constants.KMAP_RECT_SIZES_3)

    def test_operation_symbols(self):
        self.assertEqual(Constants.OP_NOT, '!')
        self.assertEqual(Constants.OP_AND, '&')
        self.assertEqual(Constants.OP_OR, '|')
        self.assertEqual(Constants.OP_XOR, '^')
        self.assertEqual(Constants.OP_IMPL, '->')
        self.assertEqual(Constants.OP_EQUIV, '~')
        self.assertEqual(Constants.OP_OR_SYMBOL, '∨')
        self.assertEqual(Constants.OP_AND_SYMBOL, '∧')

    def test_default_outputs(self):
        self.assertEqual(Constants.DEFAULT_OUTPUT_ZERO, "0")
        self.assertEqual(Constants.DEFAULT_OUTPUT_ONE, "1")

    def test_get_variables_up_to(self):
        self.assertEqual(Constants.get_variables_up_to(3), ['a', 'b', 'c'])
        self.assertEqual(Constants.get_variables_up_to(5), ['a', 'b', 'c', 'd', 'e'])

    def test_get_kmap_order(self):
        self.assertEqual(Constants.get_kmap_order(2), Constants.KMAP_ORDER_2)
        self.assertEqual(Constants.get_kmap_order(3), Constants.KMAP_ORDER_2)
        self.assertEqual(Constants.get_kmap_order(4), Constants.KMAP_ORDER_2)
        self.assertEqual(Constants.get_kmap_order(5), Constants.KMAP_ORDER_4)

    def test_get_rect_sizes(self):
        self.assertEqual(Constants.get_rect_sizes(2), Constants.KMAP_RECT_SIZES_2)
        self.assertEqual(Constants.get_rect_sizes(3), Constants.KMAP_RECT_SIZES_3)
        self.assertEqual(Constants.get_rect_sizes(4), Constants.KMAP_RECT_SIZES_4)
        self.assertEqual(Constants.get_rect_sizes(5), Constants.KMAP_RECT_SIZES_5)


if __name__ == '__main__':
    unittest.main()
