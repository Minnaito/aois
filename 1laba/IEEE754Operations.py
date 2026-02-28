from BitUtils import BitUtils


class IEEE754Operations:
    """Класс для работы с числами в формате IEEE-754 binary32"""

    def __init__(self):
        self.utils = BitUtils()
        self.bits = 32
        self.bias = 127

    def _int_to_bits(self, num, width):
        """Ручное преобразование целого числа в биты"""
        bits = [0] * width
        i = width - 1
        temp = num
        while temp > 0 and i >= 0:
            remainder = temp % 2
            bits[i] = remainder
            temp = temp // 2
            i -= 1
        return bits

    def _bits_to_int(self, bits):
        """Ручное преобразование битов в целое число"""
        val = 0
        power = 1
        for i in range(len(bits) - 1, -1, -1):
            if bits[i] == 1:
                val += power
            power *= 2
        return val

    def _multiply_by_power_of_two(self, num, power):
        """Умножение числа на 2^power без использования **"""
        if power > 0:
            for _ in range(power):
                num *= 2
        elif power < 0:
            for _ in range(-power):
                num /= 2
        return num

    def decompose(self, bits):
        """Из 32 бит возвращает (sign, exp, mant) как целые"""
        if len(bits) != self.bits:
            raise ValueError(f"Должно быть {self.bits} бита")

        sign = bits[0]
        exp = self._bits_to_int(bits[1:9])
        mant = self._bits_to_int(bits[9:])
        return sign, exp, mant

    def compose(self, sign, exp, mant):
        """Собирает 32 бита из полей"""
        result = [sign]
        result.extend(self._int_to_bits(exp, 8))
        result.extend(self._int_to_bits(mant, 23))
        return result

    def _normalize_number(self, x):
        """Нормализация числа: находит порядок и мантиссу"""
        if x == 0:
            return 0, 0

        p = 0
        if x >= 2:
            while x >= 2:
                x /= 2
                p += 1
        elif x < 1:
            while x < 1:
                x *= 2
                p -= 1

        return x, p

    def _float_to_frac_bits(self, frac, num_bits):
        """Преобразование дробной части в биты"""
        bits = [0] * num_bits
        for i in range(num_bits):
            frac *= 2
            if frac >= 1:
                bits[i] = 1
                frac -= 1
        return bits

    def float_to_bits(self, x):
        """Преобразование вещественного числа в 32-битный IEEE-754"""
        if x == 0.0:
            return [0] * self.bits

        sign = 0
        if x < 0:
            sign = 1
            x = -x

        mantissa, exponent = self._normalize_number(x)

        exp = exponent + self.bias

        if exp >= 255:
            exp = 255
            mant = 0
        elif exp <= 0:
            exp = 0
            mant = 0
        else:
            frac = mantissa - 1
            mant = 0
            frac_bits = self._float_to_frac_bits(frac, 23)
            mant = self._bits_to_int(frac_bits)

        return self.compose(sign, exp, mant)

    def _bits_to_float_value(self, sign, exp, mant):
        """Преобразование полей IEEE-754 в число"""
        # Особые случаи
        if exp == 0 and mant == 0:
            return 0.0 if sign == 0 else -0.0
        if exp == 255:
            if mant == 0:
                return float('inf') if sign == 0 else float('-inf')
            else:
                return float('nan')

        mantissa = 1 + mant / (1 << 23)

        power = exp - self.bias
        value = self._multiply_by_power_of_two(mantissa, power)

        return -value if sign else value

    def bits_to_float(self, bits):
        """Преобразование 32 бит IEEE-754 в число"""
        sign, exp, mant = self.decompose(bits)
        return self._bits_to_float_value(sign, exp, mant)

    def _add_floats(self, f1, f2):
        """Сложение двух вещественных чисел"""
        s1, e1, m1 = self.decompose(f1)
        s2, e2, m2 = self.decompose(f2)

        v1 = self._bits_to_float_value(s1, e1, m1)
        v2 = self._bits_to_float_value(s2, e2, m2)

        result = v1 + v2

        return self.float_to_bits(result)

    def add(self, bits1, bits2):
        """Сложение двух чисел в формате IEEE-754"""
        return self._add_floats(bits1, bits2)

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

        if v2 == 0:
            raise ZeroDivisionError("Деление на ноль")

        result = v1 / v2
        return self.float_to_bits(result)

    def compare(self, bits1, bits2):
        """Сравнение двух чисел в формате IEEE-754"""
        v1 = self.bits_to_float(bits1)
        v2 = self.bits_to_float(bits2)

        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
        else:
            return 0

    def is_nan(self, bits):
        """Проверка, является ли число NaN"""
        _, exp, mant = self.decompose(bits)
        return exp == 255 and mant != 0

    def is_inf(self, bits):
        """Проверка, является ли число бесконечностью"""
        _, exp, mant = self.decompose(bits)
        return exp == 255 and mant == 0

    def negate(self, bits):
        """Изменение знака числа"""
        result = bits.copy()
        result[0] = 1 if bits[0] == 0 else 0
        return result