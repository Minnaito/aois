import unittest
import math
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from IEEE754Operations import IEEE754Operations


class TestIEEE754Operations(unittest.TestCase):
    """Тесты для класса IEEE754Operations"""

    def setUp(self):
        self.ieee = IEEE754Operations()

    def test_float_to_bits_zero(self):
        """Тест преобразования нуля"""
        bits = self.ieee.float_to_bits(0.0)
        self.assertTrue(all(b == 0 for b in bits))
        self.assertEqual(self.ieee.bits_to_float(bits), 0.0)

    def test_float_to_bits_positive(self):
        """Тест преобразования положительных чисел"""
        test_cases = [1.0, 2.0, 3.14159, 1e10, 1e-10]
        for num in test_cases:
            with self.subTest(num=num):
                bits = self.ieee.float_to_bits(num)
                result = self.ieee.bits_to_float(bits)
                self.assertAlmostEqual(result, num, places=6)

    def test_float_to_bits_negative(self):
        """Тест преобразования отрицательных чисел"""
        test_cases = [-1.0, -2.5, -3.14159]
        for num in test_cases:
            with self.subTest(num=num):
                bits = self.ieee.float_to_bits(num)
                result = self.ieee.bits_to_float(bits)
                self.assertAlmostEqual(result, num, places=6)

    def test_decompose_compose(self):
        """Тест разбора и сборки числа"""
        num = 123.456
        bits = self.ieee.float_to_bits(num)
        sign, exp, mant = self.ieee.decompose(bits)
        new_bits = self.ieee.compose(sign, exp, mant)
        self.assertEqual(bits, new_bits)

    def test_special_values(self):
        """Тест специальных значений"""
        # Бесконечность
        inf_bits = [0, 1, 1, 1, 1, 1, 1, 1, 1] + [0] * 23
        inf = self.ieee.bits_to_float(inf_bits)
        self.assertTrue(math.isinf(inf))

        # NaN
        nan_bits = [0, 1, 1, 1, 1, 1, 1, 1, 1] + [1] * 23
        nan = self.ieee.bits_to_float(nan_bits)
        self.assertTrue(math.isnan(nan))

    def test_ieee754_add(self):
        """Тест сложения в IEEE-754"""
        test_cases = [
            (1.0, 2.0, 3.0),
            (1.5, 2.5, 4.0),
            (-1.0, 1.0, 0.0),
            (1e10, 1e10, 2e10),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                bits1 = self.ieee.float_to_bits(a)
                bits2 = self.ieee.float_to_bits(b)
                bits_res = self.ieee.add(bits1, bits2)
                result = self.ieee.bits_to_float(bits_res)
                self.assertAlmostEqual(result, expected, places=6)

    def test_ieee754_subtract(self):
        """Тест вычитания в IEEE-754"""
        test_cases = [
            (5.0, 2.0, 3.0),
            (1.0, 2.0, -1.0),
            (1e10, 1e9, 9e9),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                bits1 = self.ieee.float_to_bits(a)
                bits2 = self.ieee.float_to_bits(b)
                bits_res = self.ieee.subtract(bits1, bits2)
                result = self.ieee.bits_to_float(bits_res)
                # Увеличиваем допуск для больших чисел
                if abs(expected) > 1e9:
                    self.assertAlmostEqual(result, expected, delta=abs(expected) * 1e-6)
                else:
                    self.assertAlmostEqual(result, expected, places=6)

    def test_ieee754_multiply(self):
        """Тест умножения в IEEE-754"""
        test_cases = [
            (2.0, 3.0, 6.0),
            (1.5, 2.0, 3.0),
            (-2.0, 3.0, -6.0),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                bits1 = self.ieee.float_to_bits(a)
                bits2 = self.ieee.float_to_bits(b)
                bits_res = self.ieee.multiply(bits1, bits2)
                result = self.ieee.bits_to_float(bits_res)
                self.assertAlmostEqual(result, expected, places=6)

    def test_ieee754_divide(self):
        """Тест деления в IEEE-754"""
        test_cases = [
            (6.0, 2.0, 3.0),
            (1.0, 2.0, 0.5),
            (-6.0, 2.0, -3.0),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                bits1 = self.ieee.float_to_bits(a)
                bits2 = self.ieee.float_to_bits(b)
                bits_res = self.ieee.divide(bits1, bits2)
                result = self.ieee.bits_to_float(bits_res)
                self.assertAlmostEqual(result, expected, places=6)


if __name__ == '__main__':
    unittest.main()