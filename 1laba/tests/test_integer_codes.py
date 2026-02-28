import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from IntegerCodes import IntegerCodes


class TestIntegerCodes(unittest.TestCase):
    """Тесты для класса IntegerCodes"""

    def setUp(self):
        self.codes = IntegerCodes()
        self.bits = self.codes.bits
        self.max_positive = (1 << (self.bits - 1)) - 1
        self.min_negative = -(1 << (self.bits - 1))

    def test_sign_magnitude_positive_zero(self):
        """Тест прямого кода для +0"""
        bits = self.codes.int_to_sign_magnitude(0)
        self.assertEqual(bits[0], 0)
        self.assertTrue(all(b == 0 for b in bits[1:]))
        self.assertEqual(self.codes.sign_magnitude_to_int(bits), 0)

    def test_sign_magnitude_positive(self):
        """Тест прямого кода для положительных чисел"""
        test_cases = [1, 42, self.max_positive]
        for num in test_cases:
            with self.subTest(num=num):
                bits = self.codes.int_to_sign_magnitude(num)
                self.assertEqual(bits[0], 0)  
                self.assertEqual(self.codes.sign_magnitude_to_int(bits), num)

    def test_sign_magnitude_negative(self):
        """Тест прямого кода для отрицательных чисел"""
        test_cases = [-1, -42, -self.max_positive]
        for num in test_cases:
            with self.subTest(num=num):
                bits = self.codes.int_to_sign_magnitude(num)
                self.assertEqual(bits[0], 1)  
                self.assertEqual(self.codes.sign_magnitude_to_int(bits), num)

    def test_sign_magnitude_overflow_positive(self):
        """Тест переполнения для положительных чисел"""
        with self.assertRaises(ValueError) as context:
            self.codes.int_to_sign_magnitude(self.max_positive + 1)
        self.assertIn("не помещается", str(context.exception))

    def test_sign_magnitude_overflow_negative(self):
        """Тест переполнения для отрицательных чисел"""
        with self.assertRaises(ValueError) as context:
            self.codes.int_to_sign_magnitude(-self.max_positive - 1)
        self.assertIn("не помещается", str(context.exception))

    def test_ones_complement_positive(self):
        """Тест обратного кода для положительных чисел"""
        test_cases = [0, 1, 42, self.max_positive]
        for num in test_cases:
            with self.subTest(num=num):
                bits = self.codes.int_to_ones_complement(num)
                self.assertEqual(bits[0], 0)
                self.assertEqual(self.codes.ones_complement_to_int(bits), num)

    def test_ones_complement_negative(self):
        """Тест обратного кода для отрицательных чисел"""
        test_cases = [-1, -42, -self.max_positive]
        for num in test_cases:
            with self.subTest(num=num):
                bits = self.codes.int_to_ones_complement(num)
                self.assertEqual(bits[0], 1)
                self.assertEqual(self.codes.ones_complement_to_int(bits), num)

    def test_ones_complement_negative_zero(self):
        """Тест обратного кода для отрицательного нуля"""
        bits = self.codes.int_to_ones_complement(0)
        self.assertEqual(self.codes.ones_complement_to_int(bits), 0)

        neg_zero_bits = [1] * self.bits
        self.assertEqual(self.codes.ones_complement_to_int(neg_zero_bits), -0)

    def test_ones_complement_overflow(self):
        """Тест переполнения для обратного кода"""
        with self.assertRaises(ValueError):
            self.codes.int_to_ones_complement(self.max_positive + 1)
        with self.assertRaises(ValueError):
            self.codes.int_to_ones_complement(-self.max_positive - 1)

    def test_twos_complement_positive(self):
        """Тест дополнительного кода для положительных чисел"""
        test_cases = [0, 1, 42, self.max_positive]
        for num in test_cases:
            with self.subTest(num=num):
                bits = self.codes.int_to_twos_complement(num)
                self.assertEqual(self.codes.twos_complement_to_int(bits), num)

    def test_twos_complement_negative(self):
        """Тест дополнительного кода для отрицательных чисел"""
        test_cases = [-1, -42, -self.max_positive, self.min_negative]
        for num in test_cases:
            with self.subTest(num=num):
                bits = self.codes.int_to_twos_complement(num)
                self.assertEqual(bits[0], 1)
                self.assertEqual(self.codes.twos_complement_to_int(bits), num)

    def test_twos_complement_min_value(self):
        """Тест дополнительного кода для минимального значения"""
        min_val = self.min_negative
        bits = self.codes.int_to_twos_complement(min_val)
        self.assertEqual(bits[0], 1)
        self.assertTrue(all(b == 0 for b in bits[1:]))
        self.assertEqual(self.codes.twos_complement_to_int(bits), min_val)

    def test_twos_complement_overflow_positive(self):
        """Тест переполнения для положительных чисел"""
        with self.assertRaises(ValueError):
            self.codes.int_to_twos_complement(self.max_positive + 1)

    def test_twos_complement_overflow_negative(self):
        """Тест переполнения для отрицательных чисел"""
        with self.assertRaises(ValueError):
            self.codes.int_to_twos_complement(self.min_negative - 1)

    def test_all_codes_consistency(self):
        """Тест согласованности всех трёх кодов"""
        test_nums = [0, 42, -42, self.max_positive, -self.max_positive]
        for num in test_nums:
            with self.subTest(num=num):
                sm_bits = self.codes.int_to_sign_magnitude(num)
                self.assertEqual(self.codes.sign_magnitude_to_int(sm_bits), num)

                oc_bits = self.codes.int_to_ones_complement(num)
                self.assertEqual(self.codes.ones_complement_to_int(oc_bits), num)

                tc_bits = self.codes.int_to_twos_complement(num)
                self.assertEqual(self.codes.twos_complement_to_int(tc_bits), num)

if __name__ == '__main__':

    unittest.main()
