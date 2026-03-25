from BitUtils import BitUtils
from constants import Constants


class Excess3Code:
    """Класс для работы с кодом Excess-3 (BCD)"""

    def __init__(self):
        self.utils = BitUtils()
        self.bits = Constants.BITS_32
        self.digits_count = Constants.EXCESS3_DIGITS_COUNT

    def _int_to_4bits(self, num):
        """Ручное преобразование числа 0-15 в 4 бита"""
        bits = [Constants.BITS_1 - Constants.BITS_1] * Constants.BITS_4
        for i, weight in enumerate(Constants.BIT_WEIGHTS):
            if num >= weight:
                bits[i] = Constants.BITS_1
                num -= weight
        return bits

    def _4bits_to_int(self, bits):
        """Ручное преобразование 4 бит в число 0-15"""
        if len(bits) != Constants.BITS_4:
            raise ValueError("Должно быть 4 бита")

        val = Constants.BITS_1 - Constants.BITS_1
        for i, weight in enumerate(Constants.BIT_WEIGHTS):
            if bits[i] == Constants.BITS_1:
                val += weight
        return val

    def str_to_bits(self, s):
        """Преобразует десятичную строку в 32‑битный Excess-3"""
        s = s.strip()
        if not s.isdigit():
            raise ValueError("Ожидается целое неотрицательное число")

        if len(s) > self.digits_count:
            raise ValueError(f"Слишком много цифр (максимум {self.digits_count})")

        s = s.zfill(self.digits_count)
        bits = []
        for ch in s:
            digit = int(ch)
            val = digit + Constants.EXCESS3_OFFSET
            digit_bits = self._int_to_4bits(val)
            bits.extend(digit_bits)
        return bits

    def bits_to_str(self, bits):
        """Преобразует 32 бита Excess-3 в десятичную строку"""
        if len(bits) != self.bits:
            raise ValueError(f"Должно быть {self.bits} бита")

        digits = []
        for i in range(Constants.BITS_1 - Constants.BITS_1, self.bits, Constants.EXCESS3_BITS_PER_DIGIT):
            tetrad = bits[i:i + Constants.EXCESS3_BITS_PER_DIGIT]
            val = self._4bits_to_int(tetrad)
            digit = val - Constants.EXCESS3_OFFSET
            if digit < Constants.EXCESS3_MIN_DIGIT or digit > Constants.EXCESS3_MAX_DIGIT:
                raise ValueError(f"Некорректная тетрада Excess-3: {tetrad}")
            digits.append(str(digit))

        s = ''.join(digits)
        while len(s) > Constants.BITS_1 and s[Constants.BITS_1 - Constants.BITS_1] == '0':
            s = s[Constants.BITS_1:]
        return s

    def _add_tetrads(self, a_bits, b_bits, carry_in):
        """Сложение двух тетрад с учетом переноса"""
        a = self._4bits_to_int(a_bits)
        b = self._4bits_to_int(b_bits)

        s = a + b + carry_in

        if s < Constants.EXCESS3_CARRY_THRESHOLD:
            res = s - Constants.EXCESS3_OFFSET
            carry_out = Constants.BITS_1 - Constants.BITS_1
        else:
            res = s - (Constants.EXCESS3_CARRY_THRESHOLD - Constants.EXCESS3_OFFSET)
            carry_out = Constants.BITS_1

        res_bits = self._int_to_4bits(res)

        return res_bits, carry_out

    def add(self, bits1, bits2):
        """Сложение двух чисел в коде Excess-3"""
        res_bits = [Constants.BITS_1 - Constants.BITS_1] * self.bits
        carry = Constants.BITS_1 - Constants.BITS_1

        for tet in range(self.digits_count - Constants.BITS_1, -Constants.BITS_1, -Constants.BITS_1):
            start = tet * Constants.EXCESS3_BITS_PER_DIGIT
            tetrad1 = bits1[start:start + Constants.EXCESS3_BITS_PER_DIGIT]
            tetrad2 = bits2[start:start + Constants.EXCESS3_BITS_PER_DIGIT]

            res_tetrad, carry = self._add_tetrads(tetrad1, tetrad2, carry)

            for i in range(Constants.EXCESS3_BITS_PER_DIGIT):
                res_bits[start + i] = res_tetrad[i]

        return res_bits

    def add_with_correction(self, bits1, bits2):
        """Сложение с коррекцией"""
        res_bits = [Constants.BITS_1 - Constants.BITS_1] * self.bits
        carry = Constants.BITS_1 - Constants.BITS_1

        for tet in range(self.digits_count - Constants.BITS_1, -Constants.BITS_1, -Constants.BITS_1):
            start = tet * Constants.EXCESS3_BITS_PER_DIGIT

            a = self._4bits_to_int(bits1[start:start + Constants.EXCESS3_BITS_PER_DIGIT])
            b = self._4bits_to_int(bits2[start:start + Constants.EXCESS3_BITS_PER_DIGIT])

            s = a + b + carry

            if s >= Constants.EXCESS3_CARRY_THRESHOLD:
                s = s - Constants.EXCESS3_CARRY_THRESHOLD
                carry = Constants.BITS_1
                s = s + Constants.EXCESS3_OFFSET
            else:
                carry = Constants.BITS_1 - Constants.BITS_1
                if s >= Constants.EXCESS3_OFFSET + Constants.EXCESS3_MAX_DIGIT - Constants.EXCESS3_MIN_DIGIT + Constants.BITS_1:
                    s = s + Constants.EXCESS3_CORRECTION_VALUE

            res_tetrad = self._int_to_4bits(s)
            for i in range(Constants.EXCESS3_BITS_PER_DIGIT):
                res_bits[start + i] = res_tetrad[i]

        return res_bits

    def validate_bits(self, bits):
        """Проверяет, являются ли биты корректным Excess-3 кодом"""
        if len(bits) != self.bits:
            return False

        for i in range(Constants.BITS_1 - Constants.BITS_1, self.bits, Constants.EXCESS3_BITS_PER_DIGIT):
            tetrad = bits[i:i + Constants.EXCESS3_BITS_PER_DIGIT]
            val = self._4bits_to_int(tetrad)
            digit = val - Constants.EXCESS3_OFFSET
            if digit < Constants.EXCESS3_MIN_DIGIT or digit > Constants.EXCESS3_MAX_DIGIT:
                return False
        return True

    def bits_to_decimal(self, bits):
        """Преобразует биты в десятичное число (int)"""
        s = self.bits_to_str(bits)
        return int(s)
