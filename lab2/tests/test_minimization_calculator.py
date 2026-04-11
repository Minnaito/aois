import unittest
from src.MinimizationCalculator import MinimizationCalculator


class TestMinimizationCalculator(unittest.TestCase):
    def test_minimize_sdnf_and(self):
        minimizer = MinimizationCalculator([3], ['a','b'])
        self.assertEqual(minimizer.get_minimized_function(), "(a ∧ b)")

    def test_minimize_sdnf_or(self):
        minimizer = MinimizationCalculator([1,2,3], ['a','b'])
        result = minimizer.get_minimized_function()
        self.assertEqual(result, "(a ∨ b)")

    def test_minimize_sdnf_constant_zero(self):
        minimizer = MinimizationCalculator([], ['a'])
        self.assertEqual(minimizer.get_minimized_function(), "0")

    def test_minimize_sdnf_constant_one(self):
        minimizer = MinimizationCalculator([0,1], ['a'])
        self.assertEqual(minimizer.get_minimized_function(), "1")

    def test_print_result(self):
        minimizer = MinimizationCalculator([3], ['a','b'])
        minimizer.print_result()

    def test_covers_method(self):
        minimizer = MinimizationCalculator([1,2,3], ['a','b'])
        self.assertTrue(minimizer._covers("1X", "10"))
        self.assertTrue(minimizer._covers("1X", "11"))
        self.assertFalse(minimizer._covers("1X", "00"))

    def test_glue_terms(self):
        minimizer = MinimizationCalculator([], ['a','b'])
        self.assertEqual(minimizer._glue_terms("10", "11"), "1X")
        self.assertEqual(minimizer._glue_terms("10", "01"), "XX")


if __name__ == '__main__':
    unittest.main()
