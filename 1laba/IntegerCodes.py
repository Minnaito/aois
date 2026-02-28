from BitUtils import BitUtils


class IntegerCodes:
    """Класс для работы с целочисленными кодами: прямой, обратный, дополнительный"""

    def __init__(self):
        self.utils = BitUtils()
        self.bits = 32

    def _int_to_bits_manual(self, num, width):
        """Ручное преобразование целого числа в биты"""
        bits = [0] * width
        if num == 0:
            return bits

        i = width - 1
        temp = num
        while temp > 0 and i >= 0:
            remainder = temp % 2
            bits[i] = remainder
            temp = temp // 2
            i -= 1
        return bits

    def _bits_to_int_manual(self, bits):
        """Ручное преобразование битов в целое число"""
        val = 0
        power = 1
        for i in range(len(bits) - 1, -1, -1):
            if bits[i] == 1:
                val += power
            power *= 2
        return val

    def _power_of_two(self, exp):
        """Вычисление 2^exp без оператора << и **"""
        result = 1
        for _ in range(exp):
            result *= 2
        return result

    def _invert_bits(self, bits):
        """Инвертирование битов (0->1, 1->0)"""
        return [1 - b for b in bits]

    def int_to_sign_magnitude(self, n):
        """Целое число -> прямой код"""
        max_mag = self._power_of_two(self.bits - 1) - 1

        if n < -max_mag or n > max_mag:
            raise ValueError(f"Число {n} не помещается в {self.bits}-битный прямой код")

        if n == 0:
            return [0] * self.bits

        sign = 0 if n > 0 else 1

        mag = abs(n)

        mag_bits = self._int_to_bits_manual(mag, self.bits - 1)

        return [sign] + mag_bits

    def sign_magnitude_to_int(self, bits):
        """Массив битов в прямом коде -> целое число"""
        if len(bits) != self.bits:
            raise ValueError(f"Должно быть {self.bits} бит")

        sign = bits[0]
        mag = self._bits_to_int_manual(bits[1:])

        return mag if sign == 0 else -mag

    def int_to_ones_complement(self, n):
        """Целое число -> обратный код"""
        max_mag = self._power_of_two(self.bits - 1) - 1

        if n < -max_mag or n > max_mag:
            raise ValueError(f"Число {n} не помещается в {self.bits}-битный обратный код")

        if n >= 0:
            return [0] + self._int_to_bits_manual(n, self.bits - 1)
        else:
            mag = -n
            mag_bits = self._int_to_bits_manual(mag, self.bits - 1)
            inv_mag = self._invert_bits(mag_bits)
            return [1] + inv_mag

    def ones_complement_to_int(self, bits):
        """Обратный код -> целое число"""
        if len(bits) != self.bits:
            raise ValueError(f"Должно быть {self.bits} бит")

        sign = bits[0]
        mag_bits = bits[1:]

        if sign == 0:
            return self._bits_to_int_manual(mag_bits)
        else:
            inv = self._invert_bits(mag_bits)
            return -self._bits_to_int_manual(inv)

    def int_to_twos_complement(self, n):
        """Целое число -> дополнительный код"""
        min_val = -self._power_of_two(self.bits - 1)
        max_val = self._power_of_two(self.bits - 1) - 1

        if n < min_val or n > max_val:
            raise ValueError(f"Число {n} не помещается в {self.bits}-битный дополнительный код")

        if n >= 0:
            bits = self._int_to_bits_manual(n, self.bits)
            while len(bits) < self.bits:
                bits.insert(0, 0)
            return bits
        else:
            mag = -n
            mag_bits = self._int_to_bits_manual(mag, self.bits)

            inv_bits = self._invert_bits(mag_bits)

            result = self._binary_add_one(inv_bits)

            return result

    def _binary_add_one(self, bits):
        """Прибавление 1 к двоичному числу"""
        result = bits.copy()
        carry = 1

        for i in range(len(result) - 1, -1, -1):
            if carry == 0:
                break

            if result[i] == 0:
                result[i] = 1
                carry = 0
            else:
                result[i] = 0
                carry = 1

        return result

    def _twos_complement_to_int_positive(self, bits):
        """Вспомогательный метод для преобразования положительного дополнительного кода"""
        return self._bits_to_int_manual(bits)

    def _twos_complement_to_int_negative(self, bits):
        """Вспомогательный метод для преобразования отрицательного дополнительного кода"""
        inv_bits = self._invert_bits(bits)
        plus_one = self._binary_add_one(inv_bits)
        mag = self._bits_to_int_manual(plus_one)
        return -mag

    def twos_complement_to_int(self, bits):
        """Дополнительный код -> целое число"""
        if len(bits) != self.bits:
            raise ValueError(f"Должно быть {self.bits} бит")

        if bits[0] == 0:
            return self._twos_complement_to_int_positive(bits)
        else:
            return self._twos_complement_to_int_negative(bits)

    def add_twos_complement(self, bits1, bits2):
        """Сложение двух чисел в дополнительном коде"""
        # Преобразуем в целые числа
        n1 = self.twos_complement_to_int(bits1)
        n2 = self.twos_complement_to_int(bits2)

        result = n1 + n2

        min_val = -self._power_of_two(self.bits - 1)
        max_val = self._power_of_two(self.bits - 1) - 1

        if result < min_val or result > max_val:
            raise OverflowError("Переполнение при сложении")

        return self.int_to_twos_complement(result)

    def subtract_twos_complement(self, bits1, bits2):
        """Вычитание двух чисел в дополнительном коде"""
        n1 = self.twos_complement_to_int(bits1)
        n2 = self.twos_complement_to_int(bits2)

        result = n1 - n2

        min_val = -self._power_of_two(self.bits - 1)
        max_val = self._power_of_two(self.bits - 1) - 1

        if result < min_val or result > max_val:
            raise OverflowError("Переполнение при вычитании")

        return self.int_to_twos_complement(result)

    def compare_twos_complement(self, bits1, bits2):
        """Сравнение двух чисел в дополнительном коде"""
        n1 = self.twos_complement_to_int(bits1)
        n2 = self.twos_complement_to_int(bits2)

        if n1 < n2:
            return -1
        elif n1 > n2:
            return 1
        else:
            return 0