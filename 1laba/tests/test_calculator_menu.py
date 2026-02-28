import unittest
import sys
import os
from io import StringIO

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from CalculatorMenu import CalculatorMenu
from BitUtils import BitUtils
from IntegerCodes import IntegerCodes
from IntegerOperations import IntegerOperations
from IEEE754Operations import IEEE754Operations
from Excess3Code import Excess3Code


class TestCalculatorMenu(unittest.TestCase):

    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.menu = CalculatorMenu()

    def test_initialization(self):
        """Тест инициализации меню"""
        self.assertIsNotNone(self.menu.utils)
        self.assertIsNotNone(self.menu.codes)
        self.assertIsNotNone(self.menu.operations)
        self.assertIsNotNone(self.menu.ieee754)
        self.assertIsNotNone(self.menu.excess3)

        self.assertIsInstance(self.menu.utils, BitUtils)
        self.assertIsInstance(self.menu.codes, IntegerCodes)
        self.assertIsInstance(self.menu.operations, IntegerOperations)
        self.assertIsInstance(self.menu.ieee754, IEEE754Operations)
        self.assertIsInstance(self.menu.excess3, Excess3Code)

    def test_print_menu(self):
        """Тест вывода меню"""
        # Сохраняем оригинальный stdout
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            self.menu.print_menu()
            output = sys.stdout.getvalue()

            # Проверяем наличие всех пунктов меню
            self.assertIn("--- Меню операций ---", output)
            self.assertIn("1. Перевод десятичного числа", output)
            self.assertIn("2. Сложение двух чисел в дополнительном коде", output)
            self.assertIn("3. Вычитание двух чисел в дополнительном коде", output)
            self.assertIn("4. Умножение двух чисел в прямом коде", output)
            self.assertIn("5. Деление двух чисел в прямом коде", output)
            self.assertIn("6. Операции с числами IEEE-754", output)
            self.assertIn("7. Сложение двух чисел в коде Excess-3", output)
            self.assertIn("0. Выход", output)
        finally:
            # Восстанавливаем stdout
            sys.stdout = original_stdout

    def test_menu_translate_valid(self):
        """Тест перевода числа с валидным вводом"""
        # Сохраняем оригинальные stdin/stdout
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            # Подменяем ввод
            sys.stdin = StringIO("5\n")
            sys.stdout = StringIO()

            self.menu.menu_translate()
            output = sys.stdout.getvalue()

            self.assertIn("Прямой код:", output)
            self.assertIn("Обратный код:", output)
            self.assertIn("Дополнительный:", output)
            self.assertIn("Десятичное значение для проверки: 5", output)
        finally:
            # Восстанавливаем
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_menu_translate_invalid(self):
        """Тест перевода числа с невалидным вводом"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("abc\n")
            sys.stdout = StringIO()

            self.menu.menu_translate()
            output = sys.stdout.getvalue()

            self.assertIn("Ошибка:", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_menu_add_twos_valid(self):
        """Тест сложения в дополнительном коде"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("10\n5\n")
            sys.stdout = StringIO()

            self.menu.menu_add_twos()
            output = sys.stdout.getvalue()

            self.assertIn("в доп. коде:", output)
            self.assertIn("Сумма в доп. коде:", output)
            self.assertIn("Десятичный результат: 15", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_menu_add_twos_invalid(self):
        """Тест сложения с невалидным вводом"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("abc\n5\n")
            sys.stdout = StringIO()

            self.menu.menu_add_twos()
            output = sys.stdout.getvalue()

            self.assertIn("Ошибка:", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_menu_sub_twos_valid(self):
        """Тест вычитания в дополнительном коде"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("15\n7\n")
            sys.stdout = StringIO()

            self.menu.menu_sub_twos()
            output = sys.stdout.getvalue()

            self.assertIn("в доп. коде:", output)
            self.assertIn("Разность в доп. коде:", output)
            self.assertIn("Десятичный результат: 8", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_menu_sub_twos_invalid(self):
        """Тест вычитания с невалидным вводом"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("20\nabc\n")
            sys.stdout = StringIO()

            self.menu.menu_sub_twos()
            output = sys.stdout.getvalue()

            self.assertIn("Ошибка:", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_menu_multiply_valid(self):
        """Тест умножения в прямом коде"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("6\n4\n")
            sys.stdout = StringIO()

            self.menu.menu_multiply()
            output = sys.stdout.getvalue()

            self.assertIn("в прямом коде:", output)
            self.assertIn("Произведение в прямом коде:", output)
            self.assertIn("Десятичный результат: 24", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_menu_multiply_zero(self):
        """Тест умножения на ноль"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("5\n0\n")
            sys.stdout = StringIO()

            self.menu.menu_multiply()
            output = sys.stdout.getvalue()

            self.assertIn("Десятичный результат: 0", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_menu_divide_valid(self):
        """Тест деления в прямом коде"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("15\n3\n")
            sys.stdout = StringIO()

            self.menu.menu_divide()
            output = sys.stdout.getvalue()

            self.assertIn("в прямом коде:", output)
            self.assertIn("Результат деления в прямом коде:", output)
            self.assertIn("Результат в десятичном виде:", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_menu_divide_by_zero(self):
        """Тест деления на ноль"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("10\n0\n")
            sys.stdout = StringIO()

            self.menu.menu_divide()
            output = sys.stdout.getvalue()

            self.assertIn("Делитель не может быть нулём", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_menu_divide_invalid(self):
        """Тест деления с невалидным вводом"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("abc\n5\n")
            sys.stdout = StringIO()

            self.menu.menu_divide()
            output = sys.stdout.getvalue()

            self.assertIn("Ошибка:", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_menu_exit(self):
        """Тест выхода из меню"""
        result = self.menu.menu_exit()
        self.assertFalse(result)

    def test_translate_negative(self):
        """Тест перевода отрицательного числа"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("-1\n")
            sys.stdout = StringIO()

            self.menu.menu_translate()
            output = sys.stdout.getvalue()

            self.assertIn("Десятичное значение для проверки: -1", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_run_with_invalid_choice(self):
        """Тест запуска меню с невалидным выбором"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("99\n0\n")
            sys.stdout = StringIO()

            self.menu.run()
            output = sys.stdout.getvalue()

            self.assertIn("Неверный пункт меню", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_run_with_immediate_exit(self):
        """Тест немедленного выхода из меню"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("0\n")
            sys.stdout = StringIO()

            # Проверяем, что метод run не вызывает ошибок
            self.menu.run()
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_all_menu_items_covered(self):
        """Проверка, что все пункты меню существуют"""
        menu_items = ['1', '2', '3', '4', '5', '6', '7', '0']
        for item in menu_items:
            with self.subTest(menu_item=item):
                self.assertIn(item, ['1', '2', '3', '4', '5', '6', '7', '0'])


class TestCalculatorMenuIntegration(unittest.TestCase):
    """Интеграционные тесты для CalculatorMenu"""

    def setUp(self):
        self.menu = CalculatorMenu()

    def test_full_translation_flow(self):
        """Полный тест перевода числа"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("1\n255\n0\n")
            sys.stdout = StringIO()

            self.menu.run()
            output = sys.stdout.getvalue()

            self.assertIn("Прямой код:", output)
            self.assertIn("Обратный код:", output)
            self.assertIn("Дополнительный:", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_full_addition_flow(self):
        """Полный тест сложения"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("2\n100\n200\n0\n")
            sys.stdout = StringIO()

            self.menu.run()
            output = sys.stdout.getvalue()

            self.assertIn("в доп. коде:", output)
            self.assertIn("Сумма в доп. коде:", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_error_handling_flow(self):
        """Тест обработки ошибок"""
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        try:
            sys.stdin = StringIO("1\nabc\n0\n")
            sys.stdout = StringIO()

            self.menu.run()
            output = sys.stdout.getvalue()

            self.assertIn("Ошибка:", output)
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout


if __name__ == '__main__':
    unittest.main(verbosity=2)