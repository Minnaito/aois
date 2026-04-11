import unittest
from src.TruthTable import TruthTable
from src.ExpressionParser import BooleanExpressionParser
from src.constants import Constants


class TestTruthTable(unittest.TestCase):
    def setUp(self):
        self.parser = BooleanExpressionParser()

    def test_build_single_variable(self):
        tt = TruthTable(['a'], 'a', self.parser)
        table = tt.get_table()
        self.assertEqual(table, [((0,), 0), ((1,), 1)])
        self.assertEqual(tt.get_result_column(), [0, 1])
        self.assertEqual(tt.get_ones_indices(), [1])
        self.assertEqual(tt.get_zeros_indices(), [0])
        self.assertEqual(tt.get_ones_sets(), [(1,)])
        self.assertEqual(tt.get_zeros_sets(), [(0,)])
        self.assertEqual(tt.get_value_at((1,)), 1)

    def test_get_value_at_invalid(self):
        """Тест получения значения для несуществующего набора"""
        tt = TruthTable(['a'], "a", self.parser)
        with self.assertRaises(ValueError):
            tt.get_value_at((1, 1))  # Неправильная размерность

    def test_build_two_variables(self):
        tt = TruthTable(['a', 'b'], 'a&b', self.parser)
        table = tt.get_table()
        expected = [
            ((0,0), 0), ((0,1), 0), ((1,0), 0), ((1,1), 1)
        ]
        self.assertEqual(table, expected)

    def test_build_constant_zero(self):
        tt = TruthTable([], '0', self.parser)
        self.assertEqual(tt.get_table(), [((), 0)])

    def test_build_constant_one(self):
        tt = TruthTable([], '1', self.parser)
        self.assertEqual(tt.get_table(), [((), 1)])

    def test_iteration(self):
        tt = TruthTable(['a'], 'a', self.parser)
        rows = list(tt)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ((0,), 0))

    def test_len(self):
        tt = TruthTable(['a', 'b'], 'a|b', self.parser)
        self.assertEqual(len(tt), 4)

    def test_get_value_at_invalid(self):
        tt = TruthTable(['a'], 'a', self.parser)
        with self.assertRaises(ValueError):
            tt.get_value_at((2,))

    def test_complex_expression(self):
        tt = TruthTable(['a', 'b'], '!(a->b)', self.parser)
        # a->b is 0 only when a=1,b=0; then ! makes it 1 only for (1,0)
        ones = tt.get_ones_sets()
        self.assertEqual(ones, [(1,0)])


if __name__ == '__main__':
    unittest.main()
