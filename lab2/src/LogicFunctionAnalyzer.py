"""Главный модуль программы - обновленная версия с константами"""

import sys
import os
from src.TruthTableGenerator import TruthTableGenerator
from src.NormalFormsBuilder import NormalFormsBuilder
from src.PostClassesAnalyzer import PostClassesAnalyzer
from src.ZhegalkinPolynomialBuilder import ZhegalkinPolynomialBuilder
from src.DummyVariableFinder import DummyVariableFinder
from src.BooleanDerivativeCalculator import BooleanDerivativeCalculator
from src.MinimizationCalculator import MinimizationCalculator
from src.MinimizationTabular import MinimizationTabular
from src.KarnaughMapMinimizer import KarnaughMapMinimizer
from src.constants import Constants


class LogicFunctionAnalyzer:
    """Главный класс анализатора логических функций"""

    def __init__(self):
        self.expression = ""
        self.variables = []
        self.truth_table = []
        self.sdnf_terms = []
        self.sknf_terms = []
        self.normal_forms_builder = None

    def clear_screen(self):
        """Очистка экрана"""
        if os.name == Constants.OS_WINDOWS:
            os.system(Constants.CLEAR_CMD_WINDOWS)
        else:
            os.system(Constants.CLEAR_CMD_UNIX)

    def wait_for_enter(self):
        """Ожидание нажатия Enter"""
        input(Constants.MSG_PRESS_ENTER)

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
        self.print_header(Constants.HEADER_INPUT)

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
            expr = input(Constants.MSG_ENTER_FUNCTION).strip()
            if expr:
                self.expression = expr
                break
            print(Constants.ERROR_EMPTY_FUNCTION)

        try:
            tt_generator = TruthTableGenerator(self.expression)
            self.variables = tt_generator.get_variables()
            self.truth_table = tt_generator.get_truth_table()

            self.normal_forms_builder = NormalFormsBuilder(self.truth_table, self.variables)
            self.sdnf_terms, self.sknf_terms = self.normal_forms_builder.get_numeric_forms()

            return True

        except Exception as e:
            print(Constants.format_error(Constants.ERROR_LOAD_FUNCTION, error=str(e)))
            self.wait_for_enter()
            return False

    def analyze_function(self):
        """Полный анализ функции"""
        self.clear_screen()
        self.print_header(Constants.format_error(Constants.HEADER_ANALYSIS, func=self.expression))

        # 1. Таблица истинности
        print(f"\n{Constants.HEADER_TRUTH_TABLE}")
        self.print_separator()
        tt_generator = TruthTableGenerator(self.expression)
        tt_generator.print_truth_table()

        # 2. СДНФ и СКНФ
        print(f"\n{Constants.HEADER_NORMAL_FORMS}")
        self.print_separator()
        self.normal_forms_builder.print_forms()

        # 3. Классы Поста
        print(f"\n{Constants.HEADER_POST_CLASSES}")
        self.print_separator()
        post_analyzer = PostClassesAnalyzer(self.truth_table, self.variables)
        post_analyzer.print_results()

        # 4. Полином Жегалкина
        print(f"\n{Constants.HEADER_ZHEGALKIN}")
        self.print_separator()
        zhegalkin_builder = ZhegalkinPolynomialBuilder(self.truth_table, self.variables)
        zhegalkin_builder.print_polynomial()

        # 5. Фиктивные переменные
        print(f"\n{Constants.HEADER_DUMMY}")
        self.print_separator()
        dummy_finder = DummyVariableFinder(self.truth_table, self.variables)
        dummy_finder.print_results()

        # 6. Булевы производные
        print(f"\n{Constants.HEADER_DERIVATIVES}")
        self.print_separator()
        derivative_calc = BooleanDerivativeCalculator(self.truth_table, self.variables)

        if len(self.variables) >= Constants.MIN_VARS_FOR_PARTIAL:
            print("\nЧастные производные:")
            for var in self.variables:
                deriv = derivative_calc.partial(var)
                print(f"  ∂f/∂{var} = {deriv}")

        if len(self.variables) >= Constants.MIN_VARS_FOR_MIXED:
            print("\nСмешанные производные (по 2 переменным):")
            for i in range(len(self.variables)):
                for j in range(i + Constants.ONE, len(self.variables)):
                    deriv = derivative_calc.mixed(self.variables[i], self.variables[j])
                    print(f"  ∂²f/∂{self.variables[i]}∂{self.variables[j]} = {deriv}")

        # 7. Минимизация расчетным методом
        print(f"\n{Constants.HEADER_MINIMIZATION_CALC}")
        self.print_separator()
        if self.sdnf_terms:
            minimizer_calc = MinimizationCalculator(self.sdnf_terms, self.variables)
            minimizer_calc.print_result()
        else:
            print(f"\n{Constants.MSG_ZERO_FUNCTION}")

        # 8. Минимизация расчетно-табличным методом
        print(f"\n{Constants.HEADER_MINIMIZATION_TAB}")
        self.print_separator()
        if self.sdnf_terms:
            minimizer_tab = MinimizationTabular(self.sdnf_terms, self.variables)
            minimizer_tab.print_result()
        else:
            print(f"\n{Constants.MSG_ZERO_FUNCTION}")

        # 9. Минимизация картами Карно
        print(f"\n{Constants.HEADER_MINIMIZATION_KMAP}")
        self.print_separator()
        kmap_minimizer = KarnaughMapMinimizer(self.truth_table, self.variables)
        kmap_minimizer.print_kmap()

        print("\n" + Constants.LINE)
        print(Constants.HEADER_ANALYSIS_END)
        print(Constants.LINE)

    def run(self):
        """Запуск программы"""
        while True:
            self.clear_screen()
            print(Constants.LINE)
            print(f"          {Constants.MENU_TITLE}")
            print(Constants.LINE)
            print("\nГЛАВНОЕ МЕНЮ:")
            print(Constants.SEPARATOR)
            print(f" {Constants.MENU_OPTION_1}")
            print(f" {Constants.MENU_OPTION_2}")
            print(Constants.SEPARATOR)

            choice = input("\nВыберите пункт меню (1-2): ").strip()

            if choice == Constants.MENU_CHOICE_1:
                if self.input_function():
                    self.analyze_function()
                    print(Constants.MSG_ANALYSIS_COMPLETE)
                    input()
            elif choice == Constants.MENU_CHOICE_2:
                self.clear_screen()
                print("\n" + Constants.LINE)
                print(f"          {Constants.MSG_THANK_YOU}")
                print(Constants.LINE + "\n")
                sys.exit(Constants.EXIT_SUCCESS)
            else:
                print(Constants.ERROR_INVALID_CHOICE)
                self.wait_for_enter()


def main():
    """Главная функция"""
    try:
        analyzer = LogicFunctionAnalyzer()
        analyzer.run()
    except KeyboardInterrupt:
        print(f"\n\n{Constants.MSG_PROGRAM_INTERRUPTED}")
        sys.exit(Constants.EXIT_SUCCESS)


if __name__ == "__main__":
    main()