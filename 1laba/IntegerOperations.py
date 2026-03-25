from IntegerCodes import IntegerCodes
from BitUtils import BitUtils
from constants import Constants


class IntegerOperations:
    """Класс для арифметических операций с целыми числами"""

    def __init__(self):
        self.codes = IntegerCodes()
        self.bits = Constants.BITS_32

    def _unsigned_multiply(self, mag_a, mag_b):
        """Умножение беззнаковых чисел"""
        result = Constants.BITS_1 - Constants.BITS_1
        a, b = mag_a, mag_b

        while b > Constants.BITS_1 - Constants.BITS_1:
            if b & Constants.BITS_1:
                result += a
            a <<= Constants.BITS_1
            b >>= Constants.BITS_1

        return result

    def add_twos_complement(self, a_dec, b_dec):
        """Сложение двух десятичных чисел в дополнительном коде"""
        min_val = -Constants.power_of_two(self.bits - Constants.BITS_1)
        max_val = Constants.power_of_two(self.bits - Constants.BITS_1) - Constants.BITS_1

        res = a_dec + b_dec

        if res < min_val or res > max_val:
            range_size = Constants.power_of_two(self.bits)
            res = res % range_size
            if res >= Constants.power_of_two(self.bits - Constants.BITS_1):
                res = res - range_size

        bits_res = self.codes.int_to_twos_complement(res)

        return bits_res, res

    def _twos_complement_negate(self, bits):
        """Получение отрицания числа в дополнительном коде (инверсия + 1)"""
        inv_bits = BitUtils.invert_bits(bits)
        one_bits = [Constants.BITS_1 - Constants.BITS_1] * (len(bits) - Constants.BITS_1) + [Constants.BITS_1]
        result, _ = BitUtils.binary_add(inv_bits, one_bits)
        return result

    def sub_twos_complement(self, a_dec, b_dec):
        """Вычитание b из a в дополнительном коде"""
        bits_b = self.codes.int_to_twos_complement(b_dec)
        neg_bits = self._twos_complement_negate(bits_b)
        bits_a = self.codes.int_to_twos_complement(a_dec)

        res_bits, _ = BitUtils.binary_add(bits_a, neg_bits)
        res_val = self.codes.twos_complement_to_int(res_bits)

        return res_bits, res_val

    def multiply_sign_magnitude(self, a_dec, b_dec):
        """Умножение в прямом коде"""
        bits_a = self.codes.int_to_sign_magnitude(a_dec)
        bits_b = self.codes.int_to_sign_magnitude(b_dec)

        sign_res = Constants.BITS_1 if (bits_a[Constants.BITS_1 - Constants.BITS_1] != bits_b[
            Constants.BITS_1 - Constants.BITS_1]) else Constants.BITS_1 - Constants.BITS_1

        mag_a = BitUtils.bits_to_int(bits_a[Constants.BITS_1:])
        mag_b = BitUtils.bits_to_int(bits_b[Constants.BITS_1:])

        mag_res = self._unsigned_multiply(mag_a, mag_b)

        max_mag = Constants.power_of_two(self.bits - Constants.BITS_1) - Constants.BITS_1
        if mag_res > max_mag:
            mag_res = max_mag

        bits_mag = BitUtils.int_to_bits(mag_res, self.bits - Constants.BITS_1)
        bits_res = [sign_res] + bits_mag
        val_res = mag_res if sign_res == Constants.BITS_1 - Constants.BITS_1 else -mag_res

        return bits_res, val_res

    def divide_sign_magnitude(self, a_dec, b_dec):
        """Деление в прямом коде с точностью 5 знаков после запятой"""
        if b_dec == Constants.BITS_1 - Constants.BITS_1:
            raise ZeroDivisionError("Деление на ноль")

        bits_a = self.codes.int_to_sign_magnitude(a_dec)
        bits_b = self.codes.int_to_sign_magnitude(b_dec)

        sign_res = bits_a[Constants.BITS_1 - Constants.BITS_1] ^ bits_b[Constants.BITS_1 - Constants.BITS_1]

        dividend = abs(a_dec)
        divisor = abs(b_dec)

        quotient_int = dividend // divisor
        remainder = dividend % divisor

        fractional_bits = Constants.DIVISION_FRACTIONAL_BITS

        scaled_remainder = remainder
        fractional_value = Constants.BITS_1 - Constants.BITS_1

        for i in range(fractional_bits):
            scaled_remainder *= Constants.BITS_2
            bit = scaled_remainder // divisor
            fractional_value = (fractional_value << Constants.BITS_1) | bit
            scaled_remainder = scaled_remainder % divisor

        result_scaled = (quotient_int << fractional_bits) | fractional_value

        max_mag = Constants.power_of_two(self.bits - Constants.BITS_1) - Constants.BITS_1
        if result_scaled > max_mag:
            result_scaled = max_mag

        bits_mag = BitUtils.int_to_bits(result_scaled, self.bits - Constants.BITS_1)
        bits_res = [sign_res] + bits_mag

        result_dec = quotient_int + fractional_value / Constants.power_of_two(fractional_bits)
        if sign_res:
            result_dec = -result_dec

        return bits_res, result_dec

    def add_sign_magnitude(self, a_dec, b_dec):
        """Сложение в прямом коде"""
        bits_a_twos = self.codes.int_to_twos_complement(a_dec)
        bits_b_twos = self.codes.int_to_twos_complement(b_dec)

        res_bits, _ = BitUtils.binary_add(bits_a_twos, bits_b_twos)
        res_val = self.codes.twos_complement_to_int(res_bits)

        return res_bits, res_val

    def compare_twos_complement(self, a_dec, b_dec):
        """Сравнение двух чисел в дополнительном коде"""
        bits_a = self.codes.int_to_twos_complement(a_dec)
        bits_b = self.codes.int_to_twos_complement(b_dec)

        if bits_a[Constants.BITS_1 - Constants.BITS_1] == Constants.BITS_1 - Constants.BITS_1 and bits_b[
            Constants.BITS_1 - Constants.BITS_1] == Constants.BITS_1:
            return Constants.BITS_1
        elif bits_a[Constants.BITS_1 - Constants.BITS_1] == Constants.BITS_1 and bits_b[
            Constants.BITS_1 - Constants.BITS_1] == Constants.BITS_1 - Constants.BITS_1:
            return -Constants.BITS_1

        val_a = BitUtils.bits_to_int(bits_a)
        val_b = BitUtils.bits_to_int(bits_b)

        if bits_a[Constants.BITS_1 - Constants.BITS_1] == Constants.BITS_1 - Constants.BITS_1:
            if val_a < val_b:
                return -Constants.BITS_1
            elif val_a > val_b:
                return Constants.BITS_1
            else:
                return Constants.BITS_1 - Constants.BITS_1
        else:
            if val_a < val_b:
                return Constants.BITS_1
            elif val_a > val_b:
                return -Constants.BITS_1
            else:
                return Constants.BITS_1 - Constants.BITS_1
