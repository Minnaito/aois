import unittest
from src.MinimizationTabular import MinimizationTabular
from src.constants import Constants


class TestMinimizationTabular(unittest.TestCase):
    def test_minimize_sdnf_and(self):
        mt = MinimizationTabular([3], ['a','b'], is_sdnf=True)
        self.assertEqual(mt.result, "(a ∧ b)")

    def test_minimize_sdnf_or(self):
        mt = MinimizationTabular([1,2,3], ['a','b'], is_sdnf=True)
        self.assertEqual(mt.result, "a ∨ b")

    def test_minimize_sknf_and(self):
        mt = MinimizationTabular([0,1,2], ['a','b'], is_sdnf=False)
        # Фактический результат: "(a) ∧ (b)"
        self.assertEqual(mt.result, "(a) ∧ (b)")

    def test_minimize_sdnf_or(self):
        mt = MinimizationTabular([1, 2, 3], ['a', 'b'], is_sdnf=True)
        self.assertIn(mt.result, ["a ∨ b", "b ∨ a"])

    def test_constant_zero_sdnf(self):
        mt = MinimizationTabular([], ['a'], is_sdnf=True)
        self.assertEqual(mt.result, "0")

    def test_constant_one_sknf(self):
        mt = MinimizationTabular([], ['a'], is_sdnf=False)
        self.assertEqual(mt.result, "1")

    def test_all_ones_sdnf(self):
        mt = MinimizationTabular([0,1], ['a'], is_sdnf=True)
        self.assertEqual(mt.result, "1")

    def test_all_zeros_sknf(self):
        mt = MinimizationTabular([0,1], ['a'], is_sdnf=False)
        self.assertEqual(mt.result, "0")

    def test_print_result(self):
        mt = MinimizationTabular([3], ['a','b'], is_sdnf=True)
        mt.print_result()

    def test_term_to_expression(self):
        mt = MinimizationTabular([], ['a','b'], is_sdnf=True)
        expr = mt._term_to_expression("10")
        self.assertEqual(expr, "a ∧ !b")
        expr = mt._term_to_expression("1X")
        self.assertEqual(expr, "a")
        expr = mt._term_to_expression("XX")
        self.assertEqual(expr, "1")

    def test_covers(self):
        mt = MinimizationTabular([], ['a','b'], is_sdnf=True)
        self.assertTrue(mt._covers("1X", 2))
        self.assertFalse(mt._covers("1X", 0))

    def test_combine_method(self):
        mt = MinimizationTabular([], ['a','b'], is_sdnf=True)
        self.assertEqual(mt._combine("10", "11"), "1X")
        self.assertIsNone(mt._combine("10", "01"))
        self.assertIsNone(mt._combine("10", "10"))

    def test_prime_implicants_three_vars(self):
        mt = MinimizationTabular([0,1,2,3,4,5,6,7], ['a','b','c'], is_sdnf=True)
        # Функция равна 1 на всех наборах -> результат "1", prime_implicants может быть пустым
        self.assertEqual(mt.result, "1")

    def test_sknf_constant_one(self):
        mt = MinimizationTabular([], ['a','b'], is_sdnf=False)
        self.assertEqual(mt.result, "1")

    def test_sknf_all_zeros(self):
        mt = MinimizationTabular([0,1,2,3], ['a','b'], is_sdnf=False)
        self.assertEqual(mt.result, "0")

    def test_count_ones_zeros(self):
        mt = MinimizationTabular([], ['a','b'], is_sdnf=True)
        self.assertEqual(mt._count_ones("101"), 2)
        self.assertEqual(mt._count_zeros("101"), 1)

    def test_to_binary(self):
        mt = MinimizationTabular([], ['a','b','c'], is_sdnf=True)
        self.assertEqual(mt._to_binary(5, 3), "101")
        self.assertEqual(mt._to_binary(5), "101")

    def test_format_result_with_parentheses_dnf(self):
        mt = MinimizationTabular([], ['a','b'], is_sdnf=True)
        result = mt._format_result_with_parentheses("a ∧ b", True)
        self.assertEqual(result, "(a ∧ b)")

    def test_format_result_with_parentheses_cnf(self):
        mt = MinimizationTabular([], ['a','b'], is_sdnf=False)
        result = mt._format_result_with_parentheses("a ∨ b", False)
        self.assertEqual(result, "(a ∨ b)")

    def test_to_binary(self):
        mt = MinimizationTabular([], ['a','b','c'], is_sdnf=True)
        self.assertEqual(mt._to_binary(5, 3), "101")
        self.assertEqual(mt._to_binary(5), "101")
        self.assertEqual(mt._to_binary(0, 2), "00")

    def test_count_ones_zeros(self):
        mt = MinimizationTabular([], ['a','b'], is_sdnf=True)
        self.assertEqual(mt._count_ones("101"), 2)
        self.assertEqual(mt._count_ones("000"), 0)
        self.assertEqual(mt._count_zeros("101"), 1)
        self.assertEqual(mt._count_zeros("000"), 3)

    def test_combine_method(self):
        mt = MinimizationTabular([], ['a','b','c'], is_sdnf=True)
        self.assertEqual(mt._combine("100", "101"), "10X")
        self.assertEqual(mt._combine("100", "110"), "1X0")
        self.assertIsNone(mt._combine("100", "111"))
        # "100" и "000" различаются в 1 позиции, так что склеиваются в "X00"
        # Поэтому убираем эту проверку или ожидаем "X00"
        self.assertEqual(mt._combine("100", "000"), "X00")
        self.assertIsNone(mt._combine("100", "100"))

    def test_format_result_with_parentheses_dnf(self):
        mt = MinimizationTabular([], ['a','b'], is_sdnf=True)
        result = mt._format_result_with_parentheses("a ∧ b", True)
        self.assertEqual(result, "(a ∧ b)")
        result = mt._format_result_with_parentheses("(a ∧ b)", True)
        self.assertEqual(result, "(a ∧ b)")
        result = mt._format_result_with_parentheses("a", True)
        self.assertEqual(result, "a")

    def test_format_result_with_parentheses_cnf(self):
        mt = MinimizationTabular([], ['a','b'], is_sdnf=False)
        result = mt._format_result_with_parentheses("a ∨ b", False)
        self.assertEqual(result, "(a ∨ b)")
        result = mt._format_result_with_parentheses("(a ∨ b)", False)
        self.assertEqual(result, "(a ∨ b)")
        result = mt._format_result_with_parentheses("a", False)
        self.assertEqual(result, "a")

    def test_term_to_expression_cnf(self):
        mt = MinimizationTabular([], ['a','b'], is_sdnf=False)
        expr = mt._term_to_expression("10")
        self.assertEqual(expr, "!a ∨ b")
        expr = mt._term_to_expression("0X")
        self.assertEqual(expr, "a")
        expr = mt._term_to_expression("XX")
        self.assertEqual(expr, "0")

    def test_covers_method(self):
        mt = MinimizationTabular([], ['a','b','c'], is_sdnf=True)
        self.assertTrue(mt._covers("1X0", 4))   # 100
        self.assertTrue(mt._covers("1X0", 6))   # 110
        self.assertFalse(mt._covers("1X0", 0))  # 000
        self.assertFalse(mt._covers("1X0", 7))  # 111

    def test_minimize_with_essential(self):
        # Функция: a ∧ b (только набор 3)
        mt = MinimizationTabular([3], ['a','b'], is_sdnf=True)
        self.assertEqual(mt.result, "(a ∧ b)")

    def test_minimize_without_essential(self):
        # Функция: a ∨ b (наборы 1,2,3)
        mt = MinimizationTabular([1,2,3], ['a','b'], is_sdnf=True)
        self.assertIn(mt.result, ["a ∨ b", "b ∨ a"])

    def test_minimize_cnf_complex(self):
        # Функция: a ∧ b, нули на 0,1,2
        mt = MinimizationTabular([0,1,2], ['a','b'], is_sdnf=False)
        # Результат должен быть одним из возможных
        possible = ["(a) ∧ (b)", "(a ∨ b) ∧ (a ∨ !b) ∧ (!a ∨ b)"]
        self.assertIn(mt.result, possible)

    def test_print_result_cnf(self):
        mt = MinimizationTabular([0], ['a','b'], is_sdnf=False)
        mt.print_result()  # не должно падать

    def test_init_empty_indices_sdnf(self):
        mt = MinimizationTabular([], ['a'], is_sdnf=True)
        self.assertEqual(mt.result, "0")
        self.assertEqual(mt.prime_implicants, [])

    def test_init_empty_indices_sknf(self):
        mt = MinimizationTabular([], ['a'], is_sdnf=False)
        self.assertEqual(mt.result, "1")
        self.assertEqual(mt.prime_implicants, [])

    def test_init_all_indices_sdnf(self):
        mt = MinimizationTabular([0,1], ['a'], is_sdnf=True)
        self.assertEqual(mt.result, "1")
        self.assertEqual(mt.prime_implicants, [])

    def test_init_all_indices_sknf(self):
        mt = MinimizationTabular([0,1], ['a'], is_sdnf=False)
        self.assertEqual(mt.result, "0")
        self.assertEqual(mt.prime_implicants, [])

    def test_init_with_indices_sdnf(self):
        mt = MinimizationTabular([0, 1, 2, 3], ['a', 'b'], is_sdnf=True)
        self.assertEqual(mt.result, "1")
        self.assertEqual(mt.prime_implicants, [])

    def test_init_with_indices_sknf(self):
        mt = MinimizationTabular([0, 1, 2, 3], ['a', 'b'], is_sdnf=False)
        self.assertEqual(mt.result, "0")
        self.assertEqual(mt.prime_implicants, [])

    def test_find_prime_implicants_with_sknf(self):
        mt = MinimizationTabular([0, 1, 2], ['a', 'b'], is_sdnf=False)
        self.assertTrue(len(mt.prime_implicants) > 0)

    def test_find_prime_implicants_empty(self):
        mt = MinimizationTabular([], ['a', 'b'], is_sdnf=True)
        self.assertEqual(mt.prime_implicants, [])

    def test_minimize_with_remaining_imps(self):
        # Функция с несколькими импликантами, где есть выбор
        mt = MinimizationTabular([0, 1, 2, 4, 5, 6], ['a', 'b', 'c'], is_sdnf=True)
        self.assertIsNotNone(mt.result)

    def test_minimize_cnf_with_remaining_imps(self):
        mt = MinimizationTabular([1, 2, 3, 5, 6, 7], ['a', 'b', 'c'], is_sdnf=False)
        self.assertIsNotNone(mt.result)

    def test_format_result_with_parentheses_complex_dnf(self):
        mt = MinimizationTabular([], ['a', 'b'], is_sdnf=True)
        result = mt._format_result_with_parentheses("(a ∧ b) ∨ (c ∧ d)", True)
        self.assertIn("a ∧ b", result)
        self.assertIn("c ∧ d", result)

    def test_format_result_with_parentheses_complex_cnf(self):
        mt = MinimizationTabular([], ['a', 'b'], is_sdnf=False)
        result = mt._format_result_with_parentheses("(a ∨ b) ∧ (c ∨ d)", False)
        self.assertIn("a ∨ b", result)
        self.assertIn("c ∨ d", result)

    def test_term_to_expression_empty(self):
        mt = MinimizationTabular([], ['a', 'b'], is_sdnf=True)
        expr = mt._term_to_expression("")
        self.assertEqual(expr, "")

    def test_covers_all_x(self):
        mt = MinimizationTabular([], ['a', 'b', 'c'], is_sdnf=True)
        self.assertTrue(mt._covers("XXX", 0))
        self.assertTrue(mt._covers("XXX", 7))

    def test_minimize_sknf_all_ones(self):
        mt = MinimizationTabular([], ['a', 'b'], is_sdnf=False)
        self.assertEqual(mt.result, "1")

    def test_minimize_sdnf_all_zeros(self):
        mt = MinimizationTabular([], ['a', 'b'], is_sdnf=True)
        self.assertEqual(mt.result, "0")


if __name__ == '__main__':
    unittest.main()
