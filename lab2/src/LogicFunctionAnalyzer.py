"""Главный модуль программы - обновленная версия с константами"""

import sys
import os
from src.constants import Constants

from src.BooleanFunction import BooleanFunction
from src.ExpressionParser import BooleanExpressionParser
from src.TruthTable import TruthTable
from src.NormalFormsBuilder import NormalFormsBuilder
from src.PostClassesAnalyzer import PostClassesAnalyzer
from src.ZhegalkinPolynomialBuilder import ZhegalkinPolynomialBuilder
from src.DummyVariableFinder import DummyVariableFinder
from src.BooleanDerivativeCalculator import BooleanDerivativeCalculator
from src.MinimizationCalculator import MinimizationCalculator
from src.MinimizationTabular import MinimizationTabular
from src.KarnaughMapMinimizer import KarnaughMapMinimizer


class LogicFunctionAnalyzer:
    """Главный класс анализатора логических функций"""

    def __init__(self):
        self.expression = ""
        self.variables = []
        self.truth_table = []
        self.sdnf_terms = []
        self.sknf_terms = []
        self.normal_forms_builder = None
        self.boolean_function = None

    def clear_screen(self):
        """Очистка экрана"""
        if os.name == Constants.OS_WINDOWS:
            os.system(Constants.CLEAR_CMD_WINDOWS)
        else:
            os.system(Constants.CLEAR_CMD_UNIX)

    def wait_for_enter(self):
        """Ожидание нажатия Enter"""
        input("Нажмите Enter для продолжения...")

    def print_header(self, title):
        """Вывод заголовка"""
        print("\n" + Constants.LINE)
        print(f" {title}")
        print(Constants.LINE)

    def print_separator(self):
        """Вывод разделителя"""
        print(Constants.SEPARATOR)

    def input_function(self):
        """Ввод логической функции"""
        self.clear_screen()
        self.print_header("ВВОД ЛОГИЧЕСКОЙ ФУНКЦИИ")

        print("\nДоступные операции:")
        print(f"  {Constants.OP_NOT}  - отрицание (NOT)")
        print(f"  {Constants.OP_AND}  - конъюнкция (AND)")
        print(f"  {Constants.OP_OR}  - дизъюнкция (OR)")
        print(f"  {Constants.OP_IMPL} - импликация (IMPLICATION)")
        print(f"  {Constants.OP_EQUIV}  - эквивалентность (EQUIVALENCE)")
        print("\nДоступные переменные: a, b, c, d, e (до 5 переменных)")
        print("\nПримеры:")
        print(f"  {Constants.EXAMPLE_1}")
        print(f"  {Constants.EXAMPLE_2}")
        print(f"  {Constants.EXAMPLE_3}")
        print(f"  {Constants.EXAMPLE_4}")

        while True:
            expr = input("Введите логическую функцию: ").strip()
            if expr:
                self.expression = expr
                break
            print("Функция не может быть пустой!")

        try:
            self.boolean_function = BooleanFunction(self.expression)
            self.variables = self.boolean_function.variables
            self.truth_table = self._convert_truth_table_format()
            self.normal_forms_builder = NormalFormsBuilder(self.truth_table, self.variables)
            self.sdnf_terms, self.sknf_terms = self.normal_forms_builder.get_numeric_forms()
            return True

        except ValueError as e:
            print(f"Ошибка при загрузке функции: {e}")
            self.wait_for_enter()
            return False
        except Exception as e:
            print(f"Ошибка при загрузке функции: {e}")
            self.wait_for_enter()
            return False

    def _convert_truth_table_format(self):
        """Преобразование таблицы истинности в формат, совместимый с существующими классами"""
        if self.boolean_function is None:
            return []

        converted_table = []
        for bits, result in self.boolean_function.truth_table:
            row = {
                'inputs': bits,
                'output': result
            }
            converted_table.append(row)
        return converted_table

    def analyze_function(self):
        """Полный анализ функции"""
        self.clear_screen()
        self.print_header(f"АНАЛИЗ ФУНКЦИИ: {self.expression}")

        print("\n1. ТАБЛИЦА ИСТИННОСТИ:")
        self.print_separator()
        self._print_truth_table()

        print("\n2. СОВЕРШЕННЫЕ НОРМАЛЬНЫЕ ФОРМЫ:")
        self.print_separator()
        self.normal_forms_builder.print_forms()

        print("\n3. КЛАССЫ ПОСТА:")
        self.print_separator()
        post_analyzer = PostClassesAnalyzer(self.truth_table, self.variables)
        post_analyzer.print_results()

        print("\n4. ПОЛИНОМ ЖЕГАЛКИНА:")
        self.print_separator()
        zhegalkin_builder = ZhegalkinPolynomialBuilder(self.truth_table, self.variables)
        zhegalkin_builder.print_polynomial()

        print("\n5. ФИКТИВНЫЕ ПЕРЕМЕННЫЕ:")
        self.print_separator()
        dummy_finder = DummyVariableFinder(self.truth_table, self.variables)
        dummy_finder.print_results()

        print("\n6. БУЛЕВЫ ПРОИЗВОДНЫЕ:")
        self.print_separator()
        derivative_calc = BooleanDerivativeCalculator(self.truth_table, self.variables)
        derivative_calc.print_all(max_order=Constants.FOUR)

        print("\n7. МИНИМИЗАЦИЯ РАСЧЕТНЫМ МЕТОДОМ:")
        self.print_separator()
        if self.sdnf_terms:
            minimizer_calc = MinimizationCalculator(self.sdnf_terms, self.variables)
            minimizer_calc.print_result()
        else:
            print("\nФункция тождественно равна 0, минимизация не требуется")

        print("\n8. МИНИМИЗАЦИЯ РАСЧЕТНО-ТАБЛИЧНЫМ МЕТОДОМ:")
        self.print_separator()

        if self.sdnf_terms:
            print(f"\n{Constants.LINE}")
            print("МИНИМИЗАЦИЯ ПО СДНФ (единицы функции)")
            print(Constants.LINE)
            minimizer_tab_sdnf = MinimizationTabular(self.sdnf_terms, self.variables, is_sdnf=True)
            minimizer_tab_sdnf.print_result()

            print("\n")

            print(f"\n{Constants.LINE}")
            print("МИНИМИЗАЦИЯ ПО СКНФ (нули функции)")
            print(Constants.LINE)
            zeros_indices = list(set(range(Constants.POWER_BASE ** len(self.variables))) - set(self.sdnf_terms))
            if zeros_indices:
                minimizer_tab_sknf = MinimizationTabular(zeros_indices, self.variables, is_sdnf=False)
                minimizer_tab_sknf.print_result()
            else:
                print("\nРезультат минимизации (СКНФ): 1")
        else:
            print("\nФункция тождественно равна 0, минимизация не требуется")

        print("\n9. МИНИМИЗАЦИЯ МЕТОДОМ КАРТ КАРНО:")
        self.print_separator()
        kmap_minimizer = KarnaughMapMinimizer(self.truth_table, self.variables)
        kmap_minimizer.print_kmap()

        print("\n" + Constants.LINE)
        print(" АНАЛИЗ ЗАВЕРШЕН")
        print(Constants.LINE)

    def _print_truth_table(self):
        """Вывод таблицы истинности"""
        if self.boolean_function is None:
            print("Таблица истинности не построена")
            return

        header = " | ".join(self.variables) + " | F"
        print(f"  {header}")
        print(f"  {'-' * len(header)}")

        for bits, result in self.boolean_function.truth_table:
            row = " | ".join(str(b) for b in bits)
            print(f"  {row} | {result}")

    def run(self):
        """Запуск программы"""
        while True:
            self.clear_screen()
            print(Constants.LINE)
            print("          АНАЛИЗАТОР ЛОГИЧЕСКИХ ФУНКЦИЙ")
            print(Constants.LINE)
            print("\nГЛАВНОЕ МЕНЮ:")
            print(Constants.SEPARATOR)
            print(" 1. Ввести логическую функцию и выполнить полный анализ")
            print(" 2. Выход из программы")
            print(Constants.SEPARATOR)

            choice = input("\nВыберите пункт меню (1-2): ").strip()

            if choice == '1':
                if self.input_function():
                    self.analyze_function()
                    print("Анализ завершен. Нажмите Enter для возврата в меню...")
                    input()
            elif choice == '2':
                self.clear_screen()
                print("\n" + Constants.LINE)
                print("          Спасибо за использование программы!")
                print(Constants.LINE + "\n")
                sys.exit(Constants.EXIT_SUCCESS)
            else:
                print("Неверный выбор! Пожалуйста, выберите 1 или 2.")
                self.wait_for_enter()


def main():
    """Главная функция"""
    try:
        analyzer = LogicFunctionAnalyzer()
        analyzer.run()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
        sys.exit(Constants.EXIT_SUCCESS)


if __name__ == "__main__":
    main()
