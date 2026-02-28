from BitUtils import BitUtils
from IntegerCodes import IntegerCodes
from IntegerOperations import IntegerOperations
from IEEE754Operations import IEEE754Operations
from Excess3Code import Excess3Code


class CalculatorMenu:

    def __init__(self):
        self.utils = BitUtils()
        self.codes = IntegerCodes()
        self.operations = IntegerOperations()
        self.ieee754 = IEEE754Operations()
        self.excess3 = Excess3Code()

    def run(self):
        while True:
            self.print_menu()
            choice = input("Выберите пункт: ").strip()

            menu_actions = {
                '1': self.menu_translate,
                '2': self.menu_add_twos,
                '3': self.menu_sub_twos,
                '4': self.menu_multiply,
                '5': self.menu_divide,
                '6': self.menu_ieee754,
                '7': self.menu_excess3,
                '0': self.menu_exit
            }

            action = menu_actions.get(choice)
            if action:
                if not action():
                    break
            else:
                print("Неверный пункт меню")

    def print_menu(self):
        print("\n--- Меню операций ---")
        print("1. Перевод десятичного числа в прямой, обратный и дополнительный коды")
        print("2. Сложение двух чисел в дополнительном коде")
        print("3. Вычитание двух чисел в дополнительном коде")
        print("4. Умножение двух чисел в прямом коде")
        print("5. Деление двух чисел в прямом коде (точность 5 знаков)")
        print("6. Операции с числами IEEE-754 (32 бит)")
        print("7. Сложение двух чисел в коде Excess-3")
        print("0. Выход")

    def menu_translate(self):
        try:
            num = int(input("Введите целое число: "))
            print("\nПрямой код:    ", self.utils.show_bits(self.codes.int_to_sign_magnitude(num)))
            print("Обратный код:  ", self.utils.show_bits(self.codes.int_to_ones_complement(num)))
            print("Дополнительный:", self.utils.show_bits(self.codes.int_to_twos_complement(num)))
            print("Десятичное значение для проверки:", num)
        except ValueError as e:
            print("Ошибка:", e)
        return True

    def menu_add_twos(self):
        try:
            a = int(input("Введите первое число: "))
            b = int(input("Введите второе число: "))
            bits_a = self.codes.int_to_twos_complement(a)
            bits_b = self.codes.int_to_twos_complement(b)
            bits_res, res_dec = self.operations.add_twos_complement(a, b)

            print(f"\n{a} в доп. коде:   {self.utils.show_bits(bits_a)}")
            print(f"{b} в доп. коде:   {self.utils.show_bits(bits_b)}")
            print(f"Сумма в доп. коде: {self.utils.show_bits(bits_res)}")
            print(f"Десятичный результат: {res_dec}")
        except ValueError as e:
            print("Ошибка:", e)
        return True

    def menu_sub_twos(self):
        try:
            a = int(input("Введите уменьшаемое: "))
            b = int(input("Введите вычитаемое: "))
            bits_a = self.codes.int_to_twos_complement(a)
            bits_b = self.codes.int_to_twos_complement(b)
            bits_res, res_dec = self.operations.sub_twos_complement(a, b)

            print(f"\n{a} в доп. коде:   {self.utils.show_bits(bits_a)}")
            print(f"{b} в доп. коде:   {self.utils.show_bits(bits_b)}")
            print(f"Разность в доп. коде: {self.utils.show_bits(bits_res)}")
            print(f"Десятичный результат: {res_dec}")
        except ValueError as e:
            print("Ошибка:", e)
        return True

    def menu_multiply(self):
        try:
            a = int(input("Введите первый множитель: "))
            b = int(input("Введите второй множитель: "))
            bits_a = self.codes.int_to_sign_magnitude(a)
            bits_b = self.codes.int_to_sign_magnitude(b)
            bits_res, res_dec = self.operations.multiply_sign_magnitude(a, b)

            print(f"\n{a} в прямом коде: {self.utils.show_bits(bits_a)}")
            print(f"{b} в прямом коде: {self.utils.show_bits(bits_b)}")
            print(f"Произведение в прямом коде: {self.utils.show_bits(bits_res)}")
            print(f"Десятичный результат: {res_dec}")
        except ValueError as e:
            print("Ошибка:", e)
        return True

    def menu_divide(self):
        try:
            a = int(input("Введите делимое: "))
            b = int(input("Введите делитель: "))
            if b == 0:
                print("Делитель не может быть нулём")
                return True

            bits_a = self.codes.int_to_sign_magnitude(a)
            bits_b = self.codes.int_to_sign_magnitude(b)
            bits_res, res_dec = self.operations.divide_sign_magnitude(a, b)

            print(f"\n{a} в прямом коде: {self.utils.show_bits(bits_a)}")
            print(f"{b} в прямом коде: {self.utils.show_bits(bits_b)}")
            print(f"Результат деления в прямом коде: {self.utils.show_bits(bits_res)}")

            # Получаем строку битов и форматируем красиво
            bits_str = ''.join(map(str, bits_res))
            formatted_bits = ' '.join([bits_str[i:i + 4] for i in range(0, 32, 4)])

            print(f"Результат в десятичном виде: {res_dec:.5f}")

        except (ValueError, ZeroDivisionError) as e:
            print("Ошибка:", e)
        return True

    def menu_ieee754(self):
        print("\nПодменю IEEE-754:")
        print("1. Сложение")
        print("2. Вычитание")
        print("3. Умножение")
        print("4. Деление")
        sub = input("Выберите операцию: ").strip()

        try:
            x1 = float(input("Введите первое число: "))
            x2 = float(input("Введите второе число: "))
            bits1 = self.ieee754.float_to_bits(x1)
            bits2 = self.ieee754.float_to_bits(x2)

            print(f"\n{x1} в IEEE-754: {self.utils.show_bits(bits1)}")
            print(f"{x2} в IEEE-754: {self.utils.show_bits(bits2)}")

            operations = {
                '1': (self.ieee754.add, "+"),
                '2': (self.ieee754.subtract, "-"),
                '3': (self.ieee754.multiply, "*"),
                '4': (self.ieee754.divide, "/")
            }

            if sub in operations:
                op_func, op_symbol = operations[sub]
                bits_res = op_func(bits1, bits2)
                res_val = self.ieee754.bits_to_float(bits_res)
                print(f"Результат {op_symbol} в IEEE-754: {self.utils.show_bits(bits_res)}")
                print(f"Десятичный результат: {res_val:.5f}")
            else:
                print("Неверный выбор")
        except Exception as e:
            print("Ошибка:", e)
        return True

    def menu_excess3(self):
        try:
            s1 = input("Введите первое десятичное число (до 8 цифр): ")
            s2 = input("Введите второе десятичное число (до 8 цифр): ")
            bits1 = self.excess3.str_to_bits(s1)
            bits2 = self.excess3.str_to_bits(s2)

            print(f"\nПервое число в Excess-3: {self.utils.show_bits(bits1)}")
            print(f"Второе число в Excess-3: {self.utils.show_bits(bits2)}")

            bits_res = self.excess3.add(bits1, bits2)
            res_str = self.excess3.bits_to_str(bits_res)

            print(f"Сумма в Excess-3:        {self.utils.show_bits(bits_res)}")
            print(f"Десятичный результат: {res_str}")
        except ValueError as e:
            print("Ошибка:", e)
        return True

    def menu_exit(self):
        return False


if __name__ == "__main__":
    app = CalculatorMenu()
    app.run()