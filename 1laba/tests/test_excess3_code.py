# tests/test_excess3_code.py
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Excess3Code import Excess3Code


class TestExcess3Code(unittest.TestCase):
    """Тесты для класса Excess3Code"""

    def setUp(self):
        self.excess3 = Excess3Code()

    def test_str_to_bits_single_digit(self):
        """Тест преобразования однозначного числа"""
        bits = self.excess3.str_to_bits("5")
        expected = [0, 0, 1, 1] * 7 + [1, 0, 0, 0]
        self.assertEqual(bits, expected)

    def test_str_to_bits_multiple_digits(self):
        """Тест преобразования многозначного числа"""
        bits = self.excess3.str_to_bits("123")
        expected = [0, 0, 1, 1] * 5 + [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0]
        self.assertEqual(bits, expected)

    def test_str_to_bits_zero(self):
        """Тест преобразования нуля"""
        bits = self.excess3.str_to_bits("0")
        expected = [0, 0, 1, 1] * 8
        self.assertEqual(bits, expected)

    def test_str_to_bits_max_digits(self):
        """Тест преобразования максимального числа цифр"""
        bits = self.excess3.str_to_bits("12345678")
        self.assertEqual(len(bits), 32)

    def test_str_to_bits_too_many_digits(self):
        """Тест ошибки при слишком большом количестве цифр"""
        with self.assertRaises(ValueError) as context:
            self.excess3.str_to_bits("123456789")
        self.assertIn("Слишком много цифр", str(context.exception))

    def test_str_to_bits_invalid_input(self):
        """Тест ошибки при нечисловом вводе"""
        with self.assertRaises(ValueError) as context:
            self.excess3.str_to_bits("abc")
        self.assertIn("Ожидается целое неотрицательное число", str(context.exception))

    def test_bits_to_str(self):
        """Тест преобразования битов обратно в строку"""
        original = "12345"
        bits = self.excess3.str_to_bits(original)
        result = self.excess3.bits_to_str(bits)
        self.assertEqual(result, original)

    def test_bits_to_str_zero(self):
        """Тест преобразования нуля"""
        bits = self.excess3.str_to_bits("0")
        result = self.excess3.bits_to_str(bits)
        self.assertEqual(result, "0")

    def test_bits_to_str_all_digits(self):
        """Тест преобразования всех цифр"""
        for digit in range(10):
            original = str(digit)
            bits = self.excess3.str_to_bits(original)
            result = self.excess3.bits_to_str(bits)
            self.assertEqual(result, original)

    def test_bits_to_str_invalid_bits_length(self):
        """Тест ошибки при неверной длине битового массива"""
        with self.assertRaises(ValueError) as context:
            self.excess3.bits_to_str([0, 0, 0, 0])
        self.assertIn("Должно быть 32 бита", str(context.exception))

    def test_bits_to_str_invalid_tetrad(self):
        """Тест ошибки при некорректной тетраде"""
        bits = [0] * 32
        # Делаем некорректную тетраду (значение < 3)
        bits[28:32] = [0, 0, 0, 0]  # 0 < 3
        with self.assertRaises(ValueError) as context:
            self.excess3.bits_to_str(bits)
        self.assertIn("Некорректная тетрада", str(context.exception))

    def test_add_excess3_simple(self):
        """Тест простого сложения в Excess-3"""
        bits1 = self.excess3.str_to_bits("5")
        bits2 = self.excess3.str_to_bits("3")
        result_bits = self.excess3.add(bits1, bits2)
        result_str = self.excess3.bits_to_str(result_bits)
        self.assertEqual(result_str, "8")

    def test_add_excess3_with_carry(self):
        """Тест сложения с переносом"""
        bits1 = self.excess3.str_to_bits("5")
        bits2 = self.excess3.str_to_bits("5")
        result_bits = self.excess3.add(bits1, bits2)
        result_str = self.excess3.bits_to_str(result_bits)
        self.assertEqual(result_str, "10")

    def test_add_excess3_multiple_carries(self):
        """Тест сложения с несколькими переносами"""
        bits1 = self.excess3.str_to_bits("999")
        bits2 = self.excess3.str_to_bits("1")
        result_bits = self.excess3.add(bits1, bits2)
        result_str = self.excess3.bits_to_str(result_bits)
        self.assertEqual(result_str, "1000")

    def test_add_excess3_large_numbers(self):
        """Тест сложения больших чисел"""
        bits1 = self.excess3.str_to_bits("5000")
        bits2 = self.excess3.str_to_bits("5000")
        result_bits = self.excess3.add(bits1, bits2)
        result_str = self.excess3.bits_to_str(result_bits)
        self.assertEqual(result_str, "10000")

    def test_add_excess3_zero(self):
        """Тест сложения с нулем"""
        bits1 = self.excess3.str_to_bits("123")
        bits2 = self.excess3.str_to_bits("0")
        result_bits = self.excess3.add(bits1, bits2)
        result_str = self.excess3.bits_to_str(result_bits)
        self.assertEqual(result_str, "123")

    def test_add_excess3_max_value(self):
        """Тест сложения максимальных значений"""
        bits1 = self.excess3.str_to_bits("99999999")
        bits2 = self.excess3.str_to_bits("1")
        result_bits = self.excess3.add(bits1, bits2)
        result_str = self.excess3.bits_to_str(result_bits)
        self.assertLessEqual(len(result_str), 8)

    def test_validate_bits_valid(self):
        """Тест проверки корректных битов"""
        bits = self.excess3.str_to_bits("12345")
        self.assertTrue(self.excess3.validate_bits(bits))

    def test_validate_bits_invalid_length(self):
        """Тест проверки битов неверной длины"""
        bits = [0, 0, 0, 0]
        self.assertFalse(self.excess3.validate_bits(bits))

    def test_validate_bits_invalid_tetrad(self):
        """Тест проверки битов с некорректной тетрадой"""
        bits = self.excess3.str_to_bits("12345")
        bits[0:4] = [0, 0, 0, 0]
        self.assertFalse(self.excess3.validate_bits(bits))

    def test_bits_to_decimal(self):
        """Тест преобразования битов в десятичное число"""
        test_cases = ["0", "5", "123", "9999", "12345678"]
        for num_str in test_cases:
            with self.subTest(num=num_str):
                bits = self.excess3.str_to_bits(num_str)
                result = self.excess3.bits_to_decimal(bits)
                self.assertEqual(result, int(num_str))

    def test_4bits_conversion_roundtrip(self):
        """Тест преобразования туда-обратно для 4-битных значений"""
        for num in range(16):
            bits = self.excess3._int_to_4bits(num)
            result = self.excess3._4bits_to_int(bits)
            self.assertEqual(result, num)

    # Тест на граничные случаи
    def test_edge_cases(self):
        """Тест граничных случаев"""
        bits_min = self.excess3.str_to_bits("0")
        self.assertEqual(self.excess3.bits_to_str(bits_min), "0")

        bits_max = self.excess3.str_to_bits("99999999")
        self.assertEqual(self.excess3.bits_to_str(bits_max), "99999999")

        bits = self.excess3.str_to_bits("00123")
        self.assertEqual(self.excess3.bits_to_str(bits), "123")


if __name__ == '__main__':
    unittest.main()