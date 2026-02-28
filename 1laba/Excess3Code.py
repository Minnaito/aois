from BitUtils import BitUtils


class Excess3Code:
    """Класс для работы с кодом Excess-3 (BCD)"""

    def __init__(self):
        self.utils = BitUtils()
        self.bits = 32
        self.digits_count = 8

    def _int_to_4bits(self, num):
        """Ручное преобразование числа 0-15 в 4 бита"""
        bits = [0, 0, 0, 0]
        if num >= 8:
            bits[0] = 1
            num -= 8
        if num >= 4:
            bits[1] = 1
            num -= 4
        if num >= 2:
            bits[2] = 1
            num -= 2
        if num >= 1:
            bits[3] = 1
        return bits

    def _4bits_to_int(self, bits):
        """Ручное преобразование 4 бит в число 0-15"""
        if len(bits) != 4:
            raise ValueError("Должно быть 4 бита")

        val = 0
        if bits[0] == 1:
            val += 8
        if bits[1] == 1:
            val += 4
        if bits[2] == 1:
            val += 2
        if bits[3] == 1:
            val += 1
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
            val = digit + 3
            digit_bits = self._int_to_4bits(val)
            bits.extend(digit_bits)
        return bits

    def bits_to_str(self, bits):
        """Преобразует 32 бита Excess-3 в десятичную строку"""
        if len(bits) != self.bits:
            raise ValueError(f"Должно быть {self.bits} бита")

        digits = []
        for i in range(0, self.bits, 4):
            tetrad = bits[i:i + 4]
            val = self._4bits_to_int(tetrad)
            digit = val - 3
            if digit < 0 or digit > 9:
                raise ValueError(f"Некорректная тетрада Excess-3: {tetrad}")
            digits.append(str(digit))

        s = ''.join(digits)
        while len(s) > 1 and s[0] == '0':
            s = s[1:]
        return s

    def _add_tetrads(self, a_bits, b_bits, carry_in):
        """Сложение двух тетрад с учетом переноса"""
        a = self._4bits_to_int(a_bits)
        b = self._4bits_to_int(b_bits)

        s = a + b + carry_in

        if s < 16:
            res = s - 3
            carry_out = 0
        else:
            res = s - 13
            carry_out = 1

        res_bits = self._int_to_4bits(res)

        return res_bits, carry_out

    def add(self, bits1, bits2):
        """Сложение двух чисел в коде Excess-3"""
        res_bits = [0] * self.bits
        carry = 0

        for tet in range(self.digits_count - 1, -1, -1):
            start = tet * 4
            tetrad1 = bits1[start:start + 4]
            tetrad2 = bits2[start:start + 4]

            res_tetrad, carry = self._add_tetrads(tetrad1, tetrad2, carry)

            for i in range(4):
                res_bits[start + i] = res_tetrad[i]

        return res_bits

    def add_with_correction(self, bits1, bits2):
        res_bits = [0] * self.bits
        carry = 0

        for tet in range(self.digits_count - 1, -1, -1):
            start = tet * 4

            a = self._4bits_to_int(bits1[start:start + 4])
            b = self._4bits_to_int(bits2[start:start + 4])

            s = a + b + carry

            if s >= 16:
                s = s - 16
                carry = 1
                s = s + 3
            else:
                carry = 0
                if s >= 10:
                    s = s + 6

            # Преобразуем результат в биты
            res_tetrad = self._int_to_4bits(s)
            for i in range(4):
                res_bits[start + i] = res_tetrad[i]

        return res_bits

    def validate_bits(self, bits):
        """Проверяет, являются ли биты корректным Excess-3 кодом"""
        if len(bits) != self.bits:
            return False

        for i in range(0, self.bits, 4):
            tetrad = bits[i:i + 4]
            val = self._4bits_to_int(tetrad)
            digit = val - 3
            if digit < 0 or digit > 9:
                return False
        return True

    def bits_to_decimal(self, bits):
        """Преобразует биты в десятичное число (int)"""
        s = self.bits_to_str(bits)
        return int(s)