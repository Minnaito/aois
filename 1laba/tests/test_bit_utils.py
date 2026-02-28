import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BitUtils import BitUtils


class TestBitUtils(unittest.TestCase):

    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.utils = BitUtils()

    def test_show_bits_empty_list(self):
        """Тест с пустым списком"""
        result = self.utils.show_bits([])
        self.assertEqual(result, "")

    def test_show_bits_single_bit(self):
        """Тест с одним битом"""
        test_cases = [
            ([0], "0"),
            ([1], "1"),
        ]
        for bits, expected in test_cases:
            with self.subTest(bits=bits):
                result = self.utils.show_bits(bits)
                self.assertEqual(result, expected)

    def test_show_bits_4_bits(self):
        """Тест с 4 битами (ровно одна группа)"""
        test_cases = [
            ([0, 0, 0, 0], "0000"),
            ([1, 1, 1, 1], "1111"),
            ([1, 0, 1, 0], "1010"),
            ([0, 1, 0, 1], "0101"),
        ]
        for bits, expected in test_cases:
            with self.subTest(bits=bits):
                result = self.utils.show_bits(bits)
                self.assertEqual(result, expected)

    def test_show_bits_8_bits(self):
        """Тест с 8 битами (две группы)"""
        test_cases = [
            ([0, 0, 0, 0, 0, 0, 0, 0], "0000 0000"),
            ([1, 1, 1, 1, 1, 1, 1, 1], "1111 1111"),
            ([1, 0, 1, 0, 1, 0, 1, 0], "1010 1010"),
            ([0, 1, 0, 1, 0, 1, 0, 1], "0101 0101"),
            ([1, 1, 0, 0, 1, 1, 0, 0], "1100 1100"),
        ]
        for bits, expected in test_cases:
            with self.subTest(bits=bits):
                result = self.utils.show_bits(bits)
                self.assertEqual(result, expected)

    def test_show_bits_16_bits(self):
        """Тест с 16 битами (четыре группы)"""
        bits = [1] * 16
        expected = "1111 1111 1111 1111"
        result = self.utils.show_bits(bits)
        self.assertEqual(result, expected)

        bits = [0] * 16
        expected = "0000 0000 0000 0000"
        result = self.utils.show_bits(bits)
        self.assertEqual(result, expected)

    def test_show_bits_32_bits(self):
        """Тест с 32 битами (восемь групп)"""
        bits = [1, 0] * 16  # Чередующиеся 1 и 0
        expected = "1010 1010 1010 1010 1010 1010 1010 1010"
        result = self.utils.show_bits(bits)
        self.assertEqual(result, expected)

    def test_show_bits_not_multiple_of_4(self):
        """Тест с количеством бит, не кратным 4"""
        test_cases = [
            ([1, 0, 1], "101"),  # 3 бита
            ([1, 0, 1, 1, 0], "1011 0"),  # 5 бит
            ([1, 1, 1, 1, 1, 1], "1111 11"),  # 6 бит
            ([1, 0, 1, 0, 1, 0, 1], "1010 101"),  # 7 бит
            ([1, 1, 1, 1, 1, 1, 1, 1, 1], "1111 1111 1"),  # 9 бит
        ]
        for bits, expected in test_cases:
            with self.subTest(bits=bits):
                result = self.utils.show_bits(bits)
                self.assertEqual(result, expected)

    def test_show_bits_mixed_values(self):
        """Тест со смешанными значениями"""
        test_cases = [
            ([1, 0, 0, 1, 1, 0, 1, 0], "1001 1010"),
            ([0, 1, 1, 1, 0, 0, 0, 1], "0111 0001"),
            ([1, 1, 0, 1, 0, 0, 1, 1], "1101 0011"),
            ([0, 0, 1, 1, 1, 1, 0, 0], "0011 1100"),
        ]
        for bits, expected in test_cases:
            with self.subTest(bits=bits):
                result = self.utils.show_bits(bits)
                self.assertEqual(result, expected)

    def test_show_bits_long_sequence(self):
        """Тест с длинной последовательностью"""
        # Создаем последовательность из 64 бит
        bits = []
        for i in range(64):
            bits.append(i % 2)  # Чередуем 0 и 1

        expected_groups = []
        for i in range(0, 64, 4):
            group = ''.join(str(b) for b in bits[i:i + 4])
            expected_groups.append(group)
        expected = ' '.join(expected_groups)

        result = self.utils.show_bits(bits)
        self.assertEqual(result, expected)
        self.assertEqual(len(result.replace(' ', '')), 64)  

    def test_show_bits_with_invalid_bits(self):
        """Тест с недопустимыми значениями битов"""
        test_cases = [
            [0, 2, 1],  
            [1, -1, 0],  
            [1, 0, 3],  
            [1, 0.5, 0],  
        ]
        for bits in test_cases:
            with self.subTest(bits=bits):
                result = self.utils.show_bits(bits)
                # Проверяем, что результат содержит эти значения как строки
                self.assertIn(str(bits[1]), result)

    def test_show_bits_formatting(self):
        """Тест форматирования результата"""
        bits = [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1]
        result = self.utils.show_bits(bits)

        groups = result.split(' ')

        for i, group in enumerate(groups[:-1]):
            self.assertEqual(len(group), 4, f"Группа {i} имеет длину {len(group)}, ожидалось 4")

        total_bits = len(result.replace(' ', ''))
        self.assertEqual(total_bits, len(bits))

    def test_show_bits_preserves_order(self):
        """Тест сохранения порядка битов"""
        bits = [1, 0, 0, 1, 1, 0, 1, 0]
        result = self.utils.show_bits(bits)

        result_without_spaces = result.replace(' ', '')
        expected = ''.join(str(b) for b in bits)
        self.assertEqual(result_without_spaces, expected)

    def test_static_method(self):
        """Тест, что метод действительно статический"""
        # Вызов через класс
        result1 = BitUtils.show_bits([1, 0, 1, 0])
        # Вызов через экземпляр
        result2 = self.utils.show_bits([1, 0, 1, 0])

        self.assertEqual(result1, result2)
        self.assertEqual(result1, "1010")


class TestBitUtilsEdgeCases(unittest.TestCase):
    """Тесты граничных случаев для BitUtils"""

    def test_show_bits_very_long(self):
        """Тест с очень длинным списком"""
        # Создаем список из 1000 бит
        bits = [1] * 1000
        result = BitUtils.show_bits(bits)
        groups = result.split(' ')
        expected_groups = (1000 + 3) // 4  
        self.assertEqual(len(groups), expected_groups)

        total_bits = len(result.replace(' ', ''))
        self.assertEqual(total_bits, 1000)

    def test_show_bits_all_zeros(self):
        """Тест со всеми нулями разной длины"""
        for length in [1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 32]:
            with self.subTest(length=length):
                bits = [0] * length
                result = BitUtils.show_bits(bits)

                for char in result:
                    self.assertIn(char, ['0', ' '])

    def test_show_bits_all_ones(self):
        """Тест со всеми единицами разной длины"""
        for length in [1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 32]:
            with self.subTest(length=length):
                bits = [1] * length
                result = BitUtils.show_bits(bits)

                for char in result:
                    self.assertIn(char, ['1', ' '])

    def test_show_bits_alternating(self):
        """Тест с чередующимися битами"""
        patterns = [
            ([1, 0] * 4, "1010 1010"),
            ([0, 1] * 4, "0101 0101"),
            ([1, 1, 0, 0] * 2, "1100 1100"),
            ([1, 0, 0, 1] * 2, "1001 1001"),
        ]
        for bits, expected in patterns:
            with self.subTest(pattern=bits[:4]):
                result = BitUtils.show_bits(bits)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
