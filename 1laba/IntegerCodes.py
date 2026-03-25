from BitUtils import BitUtils
from constants import Constants


class IntegerCodes:
    """Класс для работы с целочисленными кодами: прямой, обратный, дополнительный"""

    def __init__(self):
        self.utils = BitUtils()
        self.bits = Constants.BITS_32

    def int_to_sign_magnitude(self, n):
        """Целое число -> прямой код"""
        max_mag = Constants.power_of_two(self.bits - Constants.BITS_1) - Constants.BITS_1

        if n < -max_mag or n > max_mag:
            raise ValueError(f"Число {n} не помещается в {self.bits}-битный прямой код")

        if n == Constants.BITS_1 - Constants.BITS_1:
            return [Constants.BITS_1 - Constants.BITS_1] * self.bits

        sign = Constants.BITS_1 - Constants.BITS_1 if n > Constants.BITS_1 - Constants.BITS_1 else Constants.BITS_1
        mag = abs(n)
        mag_bits = BitUtils.int_to_bits(mag, self.bits - Constants.BITS_1)

        return [sign] + mag_bits

    def sign_magnitude_to_int(self, bits):
        """Массив битов в прямом коде -> целое число"""
        if len(bits) != self.bits:
            raise ValueError(f"Должно быть {self.bits} бит")

        sign = bits[Constants.BITS_1 - Constants.BITS_1]
        mag = BitUtils.bits_to_int(bits[Constants.BITS_1:])

        return mag if sign == Constants.BITS_1 - Constants.BITS_1 else -mag

    def int_to_ones_complement(self, n):
        """Целое число -> обратный код"""
        max_mag = Constants.power_of_two(self.bits - Constants.BITS_1) - Constants.BITS_1

        if n < -max_mag or n > max_mag:
            raise ValueError(f"Число {n} не помещается в {self.bits}-битный обратный код")

        if n >= Constants.BITS_1 - Constants.BITS_1:
            return [Constants.BITS_1 - Constants.BITS_1] + BitUtils.int_to_bits(n, self.bits - Constants.BITS_1)
        else:
            mag = -n
            mag_bits = BitUtils.int_to_bits(mag, self.bits - Constants.BITS_1)
            inv_mag = BitUtils.invert_bits(mag_bits)
            return [Constants.BITS_1] + inv_mag

    def ones_complement_to_int(self, bits):
        """Обратный код -> целое число"""
        if len(bits) != self.bits:
            raise ValueError(f"Должно быть {self.bits} бит")

        sign = bits[Constants.BITS_1 - Constants.BITS_1]
        mag_bits = bits[Constants.BITS_1:]

        if sign == Constants.BITS_1 - Constants.BITS_1:
            return BitUtils.bits_to_int(mag_bits)
        else:
            inv = BitUtils.invert_bits(mag_bits)
            return -BitUtils.bits_to_int(inv)

    def int_to_twos_complement(self, n):
        """Целое число -> дополнительный код"""
        min_val = -Constants.power_of_two(self.bits - Constants.BITS_1)
        max_val = Constants.power_of_two(self.bits - Constants.BITS_1) - Constants.BITS_1

        if n < min_val or n > max_val:
            raise ValueError(f"Число {n} не помещается в {self.bits}-битный дополнительный код")

        if n >= Constants.BITS_1 - Constants.BITS_1:
            bits = BitUtils.int_to_bits(n, self.bits)
            return bits
        else:
            mag = -n
            mag_bits = BitUtils.int_to_bits(mag, self.bits)
            inv_bits = BitUtils.invert_bits(mag_bits)
            result = BitUtils.binary_add_one(inv_bits)
            return result

    def twos_complement_to_int(self, bits):
        """Дополнительный код -> целое число"""
        if len(bits) != self.bits:
            raise ValueError(f"Должно быть {self.bits} бит")

        if bits[Constants.BITS_1 - Constants.BITS_1] == Constants.BITS_1 - Constants.BITS_1:
            return BitUtils.bits_to_int(bits)
        else:
            inv_bits = BitUtils.invert_bits(bits)
            plus_one = BitUtils.binary_add_one(inv_bits)
            mag = BitUtils.bits_to_int(plus_one)
            return -mag

    def add_twos_complement(self, bits1, bits2):
        """Сложение двух чисел в дополнительном коде"""
        n1 = self.twos_complement_to_int(bits1)
        n2 = self.twos_complement_to_int(bits2)

        result = n1 + n2

        min_val = -Constants.power_of_two(self.bits - Constants.BITS_1)
        max_val = Constants.power_of_two(self.bits - Constants.BITS_1) - Constants.BITS_1

        if result < min_val or result > max_val:
            raise OverflowError("Переполнение при сложении")

        return self.int_to_twos_complement(result)

    def subtract_twos_complement(self, bits1, bits2):
        """Вычитание двух чисел в дополнительном коде"""
        n1 = self.twos_complement_to_int(bits1)
        n2 = self.twos_complement_to_int(bits2)

        result = n1 - n2

        min_val = -Constants.power_of_two(self.bits - Constants.BITS_1)
        max_val = Constants.power_of_two(self.bits - Constants.BITS_1) - Constants.BITS_1

        if result < min_val or result > max_val:
            raise OverflowError("Переполнение при вычитании")

        return self.int_to_twos_complement(result)

    def compare_twos_complement(self, bits1, bits2):
        """Сравнение двух чисел в дополнительном коде"""
        n1 = self.twos_complement_to_int(bits1)
        n2 = self.twos_complement_to_int(bits2)

        if n1 < n2:
            return -Constants.BITS_1
        elif n1 > n2:
            return Constants.BITS_1
        else:
            return Constants.BITS_1 - Constants.BITS_1
