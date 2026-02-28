import unittest
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from IntegerCodes import IntegerCodes
from IntegerOperations import IntegerOperations


class TestIntegerOperations(unittest.TestCase):

    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.ops = IntegerOperations()
        self.codes = IntegerCodes()
        self.bits = 32
        self.min_int = -2 ** (self.bits - 1)
        self.max_int = 2 ** (self.bits - 1) - 1

    def test_initialization(self):
        """Тест инициализации"""
        self.assertIsNotNone(self.ops.codes)
        self.assertEqual(self.ops.bits, 32)
        self.assertIsInstance(self.ops.codes, IntegerCodes)

    def test_power_of_two(self):
        """Тест вычисления степени двойки"""
        test_cases = [
            (0, 1),
            (1, 2),
            (2, 4),
            (3, 8),
            (4, 16),
            (5, 32),
            (10, 1024),
        ]
        for exp, expected in test_cases:
            with self.subTest(exp=exp):
                self.assertEqual(self.ops._power_of_two(exp), expected)

    def test_binary_add(self):
        """Тест бинарного сложения"""
        test_cases = [
            ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], 0),
            ([0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 1], 0),
            ([0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 1, 0], 0),
            ([0, 0, 1, 0], [0, 0, 1, 0], [0, 1, 0, 0], 0),
            ([1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 0], 1),
        ]
        for bits1, bits2, expected_result, expected_carry in test_cases:
            with self.subTest(bits1=bits1, bits2=bits2):
                result, carry = self.ops._binary_add(bits1, bits2)
                self.assertEqual(result, expected_result)
                self.assertEqual(carry, expected_carry)

        with self.assertRaises(ValueError):
            self.ops._binary_add([1, 0], [1, 0, 0])

    def test_twos_complement_negate(self):
        """Тест отрицания в дополнительном коде"""
        test_cases = [
            ([0, 0, 0, 1], [1, 1, 1, 1]),
            ([0, 0, 1, 0], [1, 1, 1, 0]),
            ([0, 1, 0, 1], [1, 0, 1, 1]),
            ([1, 1, 1, 1], [0, 0, 0, 1]),
            ([0, 0, 0, 0], [0, 0, 0, 0]),
        ]
        for bits, expected in test_cases:
            with self.subTest(bits=bits):
                result = self.ops._twos_complement_negate(bits)
                self.assertEqual(result, expected)

    def test_add_twos_complement(self):
        """Тест сложения в дополнительном коде"""
        test_cases = [
            (5, 3, 8),
            (-5, -3, -8),
            (5, -3, 2),
            (-5, 3, -2),
            (0, 5, 5),
            (5, 0, 5),
            (0, 0, 0),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                bits, result = self.ops.add_twos_complement(a, b)
                self.assertEqual(result, expected)
                self.assertEqual(self.ops.codes.twos_complement_to_int(bits), result)

    def test_sub_twos_complement(self):
        """Тест вычитания в дополнительном коде"""
        test_cases = [
            (10, 3, 7),
            (10, -3, 13),
            (-10, 3, -13),
            (-10, -3, -7),
            (5, 5, 0),
            (0, 5, -5),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                bits, result = self.ops.sub_twos_complement(a, b)
                self.assertEqual(result, expected)
                self.assertEqual(self.ops.codes.twos_complement_to_int(bits), result)

    def test_unsigned_multiply(self):
        """Тест беззнакового умножения"""
        test_cases = [
            (0, 5, 0),
            (5, 0, 0),
            (2, 3, 6),
            (3, 5, 15),
            (12, 12, 144),
            (123, 456, 123 * 456),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                result = self.ops._unsigned_multiply(a, b)
                self.assertEqual(result, expected)

    def test_unsigned_multiply_bits(self):
        """Тест умножения битовых представлений беззнаковых чисел"""
        test_cases = [
            ([1], [1], 1),
            ([1], [0], 0),
            ([0], [1], 0),
            ([0, 0, 0, 1], [0, 0, 0, 1], 1),
            ([0, 0, 1, 0], [0, 0, 1, 1], 6),
            ([0, 1, 0, 1], [0, 0, 1, 0], 10),
        ]
        for bits_a, bits_b, expected in test_cases:
            with self.subTest(bits_a=bits_a, bits_b=bits_b):
                result = self.ops._unsigned_multiply_bits(bits_a, bits_b)
                self.assertEqual(result, expected)

    def test_multiply_sign_magnitude(self):
        """Тест умножения в прямом коде"""
        test_cases = [
            (5, 3, 15),
            (-5, 3, -15),
            (5, -3, -15),
            (-5, -3, 15),
            (0, 5, 0),
            (5, 0, 0),
            (self.max_int, 1, self.max_int),
            (self.max_int, 2, self.max_int),  # Переполнение
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                bits, result = self.ops.multiply_sign_magnitude(a, b)
                sign_bit = 1 if (a < 0) ^ (b < 0) else 0
                self.assertEqual(bits[0], sign_bit)
                self.assertEqual(result, expected)

    def test_divide_sign_magnitude(self):
        """Тест деления в прямом коде (только целочисленное деление)"""
        test_cases = [
            (10, 2, 5.0),
            (20, 5, 4.0),
            (100, 25, 4.0),
            (7, 1, 7.0),
            (-10, 2, -5.0),
            (10, -2, -5.0),
            (-10, -2, 5.0),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                bits, result = self.ops.divide_sign_magnitude(a, b)
                sign_bit = 1 if (a < 0) ^ (b < 0) else 0
                self.assertEqual(bits[0], sign_bit)
                self.assertEqual(result, expected)

        with self.assertRaises(ZeroDivisionError):
            self.ops.divide_sign_magnitude(5, 0)

    def test_add_sign_magnitude(self):
        """Тест сложения в прямом коде"""
        test_cases = [
            (5, 3, 8),
            (-5, -3, -8),
            (5, -3, 2),
            (-5, 3, -2),
            (0, 5, 5),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                bits, result = self.ops.add_sign_magnitude(a, b)
                self.assertEqual(result, expected)

    def test_compare_twos_complement(self):
        """Тест сравнения в дополнительном коде (только для положительных чисел)"""
        test_cases = [
            (5, 3, 1),
            (3, 5, -1),
            (5, 5, 0),
            (0, 5, -1),
            (5, 0, 1),
            (10, 10, 0),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                result = self.ops.compare_twos_complement(a, b)
                self.assertEqual(result, expected)

    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Ноль
        zero_twos = self.ops.codes.int_to_twos_complement(0)
        self.assertEqual(zero_twos, [0] * self.bits)

        # -1
        minus_one = self.ops.codes.int_to_twos_complement(-1)
        self.assertEqual(minus_one, [1] * self.bits)

        # Максимальное положительное
        max_pos = self.ops.codes.int_to_twos_complement(self.max_int)
        self.assertEqual(max_pos[0], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)