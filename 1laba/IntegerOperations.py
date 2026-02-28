from IntegerCodes import IntegerCodes


class IntegerOperations:
    """Класс для арифметических операций с целыми числами"""

    def __init__(self):
        self.codes = IntegerCodes()
        self.bits = 32

    def _power_of_two(self, exp):
        """Вычисление 2^exp без оператора << и **"""
        result = 1
        for _ in range(exp):
            result *= 2
        return result

    def _binary_add(self, bits1, bits2):
        """Бинарное сложение двух массивов битов"""
        if len(bits1) != len(bits2):
            raise ValueError("Размеры массивов должны совпадать")

        result = [0] * len(bits1)
        carry = 0

        for i in range(len(bits1) - 1, -1, -1):
            s = bits1[i] + bits2[i] + carry

            if s == 0:
                result[i] = 0
                carry = 0
            elif s == 1:
                result[i] = 1
                carry = 0
            elif s == 2:
                result[i] = 0
                carry = 1
            else:
                result[i] = 1
                carry = 1

        return result, carry

    def _twos_complement_negate(self, bits):
        """Получение отрицания числа в дополнительном коде (инверсия + 1)"""
        inv_bits = [1 - b for b in bits]

        result, _ = self._binary_add(inv_bits, [0] * (len(bits) - 1) + [1])

        return result

    def add_twos_complement(self, a_dec, b_dec):
        """Сложение двух десятичных чисел в дополнительном коде"""
        min_val = -self._power_of_two(self.bits - 1)
        max_val = self._power_of_two(self.bits - 1) - 1

        res = a_dec + b_dec

        if res < min_val or res > max_val:
            range_size = self._power_of_two(self.bits)
            res = res % range_size
            if res >= self._power_of_two(self.bits - 1):
                res = res - range_size

        bits_res = self.codes.int_to_twos_complement(res)

        return bits_res, res

    def sub_twos_complement(self, a_dec, b_dec):
        """Вычитание b из a в дополнительном коде"""
        bits_b = self.codes.int_to_twos_complement(b_dec)

        neg_bits = self._twos_complement_negate(bits_b)

        bits_a = self.codes.int_to_twos_complement(a_dec)

        res_bits, carry = self._binary_add(bits_a, neg_bits)

        res_val = self.codes.twos_complement_to_int(res_bits)

        return res_bits, res_val

    def _unsigned_multiply(self, mag_a, mag_b):
        """Умножение беззнаковых чисел (оптимизированная версия)"""
        result = 0
        a, b = mag_a, mag_b

        while b > 0:
            if b & 1:
                result += a
            a <<= 1
            b >>= 1

        return result

    def _unsigned_multiply_bits(self, bits_a, bits_b):
        """Умножение двух беззнаковых чисел в битовом представлении"""
        val_a = self.codes._bits_to_int_manual(bits_a)
        val_b = self.codes._bits_to_int_manual(bits_b)

        result = self._unsigned_multiply(val_a, val_b)

        return result

    def multiply_sign_magnitude(self, a_dec, b_dec):
        """Умножение в прямом коде"""
        bits_a = self.codes.int_to_sign_magnitude(a_dec)
        bits_b = self.codes.int_to_sign_magnitude(b_dec)

        sign_res = 1 if (bits_a[0] != bits_b[0]) else 0

        mag_a = self.codes._bits_to_int_manual(bits_a[1:])
        mag_b = self.codes._bits_to_int_manual(bits_b[1:])

        mag_res = self._unsigned_multiply(mag_a, mag_b)

        max_mag = self._power_of_two(self.bits - 1) - 1
        if mag_res > max_mag:
            mag_res = max_mag

        bits_mag = self.codes._int_to_bits_manual(mag_res, self.bits - 1)

        bits_res = [sign_res] + bits_mag
        val_res = mag_res if sign_res == 0 else -mag_res

        return bits_res, val_res

    def divide_sign_magnitude(self, a_dec, b_dec):
        """Деление в прямом коде с точностью 5 знаков после запятой"""
        if b_dec == 0:
            raise ZeroDivisionError("Деление на ноль")

        bits_a = self.codes.int_to_sign_magnitude(a_dec)
        bits_b = self.codes.int_to_sign_magnitude(b_dec)

        sign_res = bits_a[0] ^ bits_b[0]

        dividend = abs(a_dec)
        divisor = abs(b_dec)

        quotient_int = dividend // divisor
        remainder = dividend % divisor

        fractional_bits = 16

        scaled_remainder = remainder
        fractional_value = 0

        for i in range(fractional_bits):
            scaled_remainder *= 2
            bit = scaled_remainder // divisor
            fractional_value = (fractional_value << 1) | bit
            scaled_remainder = scaled_remainder % divisor

        result_scaled = (quotient_int << fractional_bits) | fractional_value

        max_mag = self._power_of_two(self.bits - 1) - 1
        if result_scaled > max_mag:
            result_scaled = max_mag

        bits_mag = self.codes._int_to_bits_manual(result_scaled, self.bits - 1)

        bits_res = [sign_res] + bits_mag

        result_dec = quotient_int + fractional_value / (2 ** fractional_bits)
        if sign_res:
            result_dec = -result_dec

        return bits_res, result_dec

    def add_sign_magnitude(self, a_dec, b_dec):
        """Сложение в прямом коде"""
        bits_a_twos = self.codes.int_to_twos_complement(a_dec)
        bits_b_twos = self.codes.int_to_twos_complement(b_dec)

        res_bits, _ = self._binary_add(bits_a_twos, bits_b_twos)

        res_val = self.codes.twos_complement_to_int(res_bits)

        return res_bits, res_val

    def compare_twos_complement(self, a_dec, b_dec):
        """Сравнение двух чисел в дополнительном коде"""
        bits_a = self.codes.int_to_twos_complement(a_dec)
        bits_b = self.codes.int_to_twos_complement(b_dec)

        if bits_a[0] == 0 and bits_b[0] == 1:
            return 1
        elif bits_a[0] == 1 and bits_b[0] == 0:
            return -1

        val_a = self.codes._bits_to_int_manual(bits_a)
        val_b = self.codes._bits_to_int_manual(bits_b)

        if bits_a[0] == 0:
            if val_a < val_b:
                return -1
            elif val_a > val_b:
                return 1
            else:
                return 0
        else:
            if val_a < val_b:
                return 1
            elif val_a > val_b:
                return -1
            else:
                return 0