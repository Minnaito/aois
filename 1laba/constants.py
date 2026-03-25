class Constants:
    # Базовые константы
    BITS_32 = 32
    BITS_31 = 31
    BITS_24 = 24
    BITS_23 = 23
    BITS_16 = 16
    BITS_8 = 8
    BITS_4 = 4
    BITS_2 = 2
    BITS_1 = 1

    # Константы для группировки битов
    BITS_PER_GROUP = 4

    # Константы для целочисленных кодов
    MAX_31BIT_UNSIGNED = 2147483647
    MAX_32BIT_UNSIGNED = 4294967295
    MIN_32BIT_SIGNED = -2147483648
    MAX_32BIT_SIGNED = 2147483647

    # Константы для IEEE-754
    IEEE754_BIAS = 127
    IEEE754_EXP_BITS = 8
    IEEE754_MANT_BITS = 23
    IEEE754_EXP_MAX = 255
    IEEE754_EXP_MIN = 0
    IEEE754_NORMALIZED_EXP_MIN = 1
    IEEE754_NORMALIZED_EXP_MAX = 254
    IEEE754_SIGN_BIT_INDEX = 0
    IEEE754_EXP_START = 1
    IEEE754_MANT_START = 9
    IEEE754_NAN_MANTISSA_MIN = 1

    # Константы для Excess-3
    EXCESS3_DIGITS_COUNT = 8
    EXCESS3_OFFSET = 3
    EXCESS3_MAX_DIGIT = 9
    EXCESS3_MIN_DIGIT = 0
    EXCESS3_TETRAD_VALUES = 16
    EXCESS3_CARRY_THRESHOLD = 16
    EXCESS3_CORRECTION_VALUE = 6
    EXCESS3_BITS_PER_DIGIT = 4

    # Константы для деления
    DIVISION_FRACTIONAL_BITS = 16
    DIVISION_PRECISION = 5

    # Константы для умножения
    MULTIPLICATION_BITS = 32

    # Константы для форматирования
    FORMAT_GROUP_SIZE = 4

    # Битовые веса для 4-битной тетрады
    BIT_WEIGHTS = [8, 4, 2, 1]

    # Степени двойки (предрассчитанные для оптимизации)
    POWERS_OF_TWO = [
        1, 2, 4, 8, 16, 32, 64, 128, 256, 512,
        1024, 2048, 4096, 8192, 16384, 32768,
        65536, 131072, 262144, 524288, 1048576,
        2097152, 4194304, 8388608, 16777216,
        33554432, 67108864, 134217728, 268435456,
        536870912, 1073741824, 2147483648
    ]

    # Значения для сложения битов
    BIT_SUM_VALUES = {
        0: 0,
        1: 1,
        2: 0,
        3: 1
    }

    BIT_CARRY_VALUES = {
        0: 0,
        1: 0,
        2: 1,
        3: 1
    }

    @staticmethod
    def power_of_two(exp):
        """Вычисление 2^exp"""
        if exp < 0:
            result = 1.0
            for _ in range(-exp):
                result /= 2.0
            return result
        if exp < len(Constants.POWERS_OF_TWO):
            return Constants.POWERS_OF_TWO[exp]
        result = 1
        for _ in range(exp):
            result *= 2
        return result
