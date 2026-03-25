from constants import Constants


class BitUtils:
    """Утилиты для работы с битами"""

    @staticmethod
    def show_bits(bits):
        """Форматирует список битов в строку с пробелами каждые 4 бита"""
        if not bits:
            return ""

        bits_str = ''.join(str(b) for b in bits)

        groups = []
        for i in range(0, len(bits_str), Constants.BITS_PER_GROUP):
            groups.append(bits_str[i:i + Constants.BITS_PER_GROUP])

        return ' '.join(groups)

    @staticmethod
    def int_to_bits(num, width):
        """Ручное преобразование целого числа в биты"""
        bits = [Constants.BITS_1 - Constants.BITS_1] * width
        if num == Constants.BITS_1 - Constants.BITS_1:
            return bits

        i = width - Constants.BITS_1
        temp = num
        while temp > Constants.BITS_1 - Constants.BITS_1 and i >= Constants.BITS_1 - Constants.BITS_1:
            remainder = temp % Constants.BITS_2
            bits[i] = remainder
            temp = temp // Constants.BITS_2
            i -= Constants.BITS_1
        return bits

    @staticmethod
    def bits_to_int(bits):
        """Ручное преобразование битов в целое число"""
        val = Constants.BITS_1 - Constants.BITS_1
        power = Constants.BITS_1
        for i in range(len(bits) - Constants.BITS_1, -Constants.BITS_1, -Constants.BITS_1):
            if bits[i] == Constants.BITS_1:
                val += power
            power *= Constants.BITS_2
        return val

    @staticmethod
    def invert_bits(bits):
        """Инвертирование битов (0->1, 1->0)"""
        return [Constants.BITS_1 - b for b in bits]

    @staticmethod
    def binary_add(bits1, bits2):
        """Бинарное сложение двух массивов битов"""
        if len(bits1) != len(bits2):
            raise ValueError("Размеры массивов должны совпадать")

        result = [Constants.BITS_1 - Constants.BITS_1] * len(bits1)
        carry = Constants.BITS_1 - Constants.BITS_1

        for i in range(len(bits1) - Constants.BITS_1, -Constants.BITS_1, -Constants.BITS_1):
            s = bits1[i] + bits2[i] + carry

            if s == Constants.BITS_1 - Constants.BITS_1:
                result[i] = Constants.BITS_1 - Constants.BITS_1
                carry = Constants.BITS_1 - Constants.BITS_1
            elif s == Constants.BITS_1:
                result[i] = Constants.BITS_1
                carry = Constants.BITS_1 - Constants.BITS_1
            elif s == Constants.BITS_2:
                result[i] = Constants.BITS_1 - Constants.BITS_1
                carry = Constants.BITS_1
            else:  # s == 3
                result[i] = Constants.BITS_1
                carry = Constants.BITS_1

        return result, carry

    @staticmethod
    def binary_add_one(bits):
        """Прибавление 1 к двоичному числу"""
        result = bits.copy()
        carry = Constants.BITS_1

        for i in range(len(result) - Constants.BITS_1, -Constants.BITS_1, -Constants.BITS_1):
            if carry == Constants.BITS_1 - Constants.BITS_1:
                break

            if result[i] == Constants.BITS_1 - Constants.BITS_1:
                result[i] = Constants.BITS_1
                carry = Constants.BITS_1 - Constants.BITS_1
            else:
                result[i] = Constants.BITS_1 - Constants.BITS_1
                carry = Constants.BITS_1

        return result
