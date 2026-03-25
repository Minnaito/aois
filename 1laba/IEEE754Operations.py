from BitUtils import BitUtils
from constants import Constants


class IEEE754Operations:
    """Класс для работы с числами в формате IEEE-754 binary32"""

    def __init__(self):
        self.utils = BitUtils()
        self.bits = Constants.BITS_32
        self.bias = Constants.IEEE754_BIAS

    def decompose(self, bits):
        """Из 32 бит возвращает (sign, exp, mant) как целые"""
        if len(bits) != self.bits:
            raise ValueError(f"Должно быть {self.bits} бита")

        sign = bits[Constants.IEEE754_SIGN_BIT_INDEX]
        exp = BitUtils.bits_to_int(bits[Constants.IEEE754_EXP_START:Constants.IEEE754_MANT_START])
        mant = BitUtils.bits_to_int(bits[Constants.IEEE754_MANT_START:])
        return sign, exp, mant

    def compose(self, sign, exp, mant):
        """Собирает 32 бита из полей"""
        result = [sign]
        result.extend(BitUtils.int_to_bits(exp, Constants.IEEE754_EXP_BITS))
        result.extend(BitUtils.int_to_bits(mant, Constants.IEEE754_MANT_BITS))
        return result

    def _normalize_number(self, x):
        """Нормализация числа: находит порядок и мантиссу"""
        if x == Constants.BITS_1 - Constants.BITS_1:
            return Constants.BITS_1 - Constants.BITS_1, Constants.BITS_1 - Constants.BITS_1

        p = Constants.BITS_1 - Constants.BITS_1
        if x >= Constants.BITS_2:
            while x >= Constants.BITS_2:
                x /= Constants.BITS_2
                p += Constants.BITS_1
        elif x < Constants.BITS_1:
            while x < Constants.BITS_1:
                x *= Constants.BITS_2
                p -= Constants.BITS_1

        return x, p

    def _float_to_frac_bits(self, frac, num_bits):
        """Преобразование дробной части в биты"""
        bits = [Constants.BITS_1 - Constants.BITS_1] * num_bits
        for i in range(num_bits):
            frac *= Constants.BITS_2
            if frac >= Constants.BITS_1:
                bits[i] = Constants.BITS_1
                frac -= Constants.BITS_1
        return bits

    def float_to_bits(self, x):
        """Преобразование вещественного числа в 32-битный IEEE-754"""
        if x == Constants.BITS_1 - Constants.BITS_1:
            return [Constants.BITS_1 - Constants.BITS_1] * self.bits

        sign = Constants.BITS_1 - Constants.BITS_1
        if x < Constants.BITS_1 - Constants.BITS_1:
            sign = Constants.BITS_1
            x = -x

        mantissa, exponent = self._normalize_number(x)

        exp = exponent + self.bias

        if exp >= Constants.IEEE754_EXP_MAX:
            exp = Constants.IEEE754_EXP_MAX
            mant = Constants.BITS_1 - Constants.BITS_1
        elif exp <= Constants.IEEE754_EXP_MIN:
            exp = Constants.IEEE754_EXP_MIN
            mant = Constants.BITS_1 - Constants.BITS_1
        else:
            frac = mantissa - Constants.BITS_1
            frac_bits = self._float_to_frac_bits(frac, Constants.IEEE754_MANT_BITS)
            mant = BitUtils.bits_to_int(frac_bits)

        return self.compose(sign, exp, mant)

    def _bits_to_float_value(self, sign, exp, mant):
        """Преобразование полей IEEE-754 в число"""
        if exp == Constants.IEEE754_EXP_MIN and mant == Constants.BITS_1 - Constants.BITS_1:
            return Constants.BITS_1 - Constants.BITS_1 if sign == Constants.BITS_1 - Constants.BITS_1 else -Constants.BITS_1 - Constants.BITS_1

        if exp == Constants.IEEE754_EXP_MAX:
            if mant == Constants.BITS_1 - Constants.BITS_1:
                return float('inf') if sign == Constants.BITS_1 - Constants.BITS_1 else float('-inf')
            else:
                return float('nan')

        mantissa = Constants.BITS_1 + mant / Constants.power_of_two(Constants.IEEE754_MANT_BITS)

        power = exp - self.bias
        value = mantissa * Constants.power_of_two(power)

        return -value if sign else value

    def bits_to_float(self, bits):
        """Преобразование 32 бит IEEE-754 в число"""
        sign, exp, mant = self.decompose(bits)
        return self._bits_to_float_value(sign, exp, mant)

    def add(self, bits1, bits2):
        """Сложение двух чисел в формате IEEE-754"""
        s1, e1, m1 = self.decompose(bits1)
        s2, e2, m2 = self.decompose(bits2)

        v1 = self._bits_to_float_value(s1, e1, m1)
        v2 = self._bits_to_float_value(s2, e2, m2)

        result = v1 + v2
        return self.float_to_bits(result)

    def subtract(self, bits1, bits2):
        """Вычитание двух чисел в формате IEEE-754"""
        s1, e1, m1 = self.decompose(bits1)
        s2, e2, m2 = self.decompose(bits2)

        v1 = self._bits_to_float_value(s1, e1, m1)
        v2 = self._bits_to_float_value(s2, e2, m2)

        result = v1 - v2
        return self.float_to_bits(result)

    def multiply(self, bits1, bits2):
        """Умножение двух чисел в формате IEEE-754"""
        s1, e1, m1 = self.decompose(bits1)
        s2, e2, m2 = self.decompose(bits2)

        v1 = self._bits_to_float_value(s1, e1, m1)
        v2 = self._bits_to_float_value(s2, e2, m2)

        result = v1 * v2
        return self.float_to_bits(result)

    def divide(self, bits1, bits2):
        """Деление двух чисел в формате IEEE-754"""
        s1, e1, m1 = self.decompose(bits1)
        s2, e2, m2 = self.decompose(bits2)

        v1 = self._bits_to_float_value(s1, e1, m1)
        v2 = self._bits_to_float_value(s2, e2, m2)

        if v2 == Constants.BITS_1 - Constants.BITS_1:
            raise ZeroDivisionError("Деление на ноль")

        result = v1 / v2
        return self.float_to_bits(result)

    def compare(self, bits1, bits2):
        """Сравнение двух чисел в формате IEEE-754"""
        v1 = self.bits_to_float(bits1)
        v2 = self.bits_to_float(bits2)

        if v1 < v2:
            return -Constants.BITS_1
        elif v1 > v2:
            return Constants.BITS_1
        else:
            return Constants.BITS_1 - Constants.BITS_1

    def is_nan(self, bits):
        """Проверка, является ли число NaN"""
        _, exp, mant = self.decompose(bits)
        return exp == Constants.IEEE754_EXP_MAX and mant != Constants.BITS_1 - Constants.BITS_1

    def is_inf(self, bits):
        """Проверка, является ли число бесконечностью"""
        _, exp, mant = self.decompose(bits)
        return exp == Constants.IEEE754_EXP_MAX and mant == Constants.BITS_1 - Constants.BITS_1

    def negate(self, bits):
        """Изменение знака числа"""
        result = bits.copy()
        result[Constants.IEEE754_SIGN_BIT_INDEX] = Constants.BITS_1 if bits[
                                                                           Constants.IEEE754_SIGN_BIT_INDEX] == Constants.BITS_1 - Constants.BITS_1 else Constants.BITS_1 - Constants.BITS_1
        return result
