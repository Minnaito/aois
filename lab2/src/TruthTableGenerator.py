"""Класс для построения таблицы истинности"""

from itertools import product
import re
from src.constants import Constants


class TruthTableGenerator:
    """Генератор таблицы истинности для логической функции"""

    def __init__(self, expression: str):
        self.expression = expression
        self.variables = self._extract_variables()
        self.truth_table = []
        self._generate_truth_table()

    def _extract_variables(self) -> list:
        """Извлечение переменных из выражения"""
        found_vars = set(re.findall(Constants.VARIABLE_PATTERN, self.expression))
        found_vars = {var for var in found_vars if var.lower() not in Constants.KEYWORDS}

        return sorted(list(found_vars))

    def _parse_expression(self, expr: str, values: dict) -> bool:
        """Парсинг и вычисление логического выражения"""
        local_expr = expr

        for var, val in values.items():
            local_expr = local_expr.replace(var, str(val))

        while Constants.OP_IMPL in local_expr:
            match = re.search(Constants.OP_IMPL_PATTERN, local_expr)
            if match:
                left, right = match.group(Constants.FIRST_GROUP), match.group(Constants.SECOND_GROUP)
                local_expr = local_expr.replace(match.group(Constants.ZERO_GROUP),
                                                f'(not {left} or {right})')
            else:
                break

        local_expr = local_expr.replace(Constants.OP_NOT, f' {Constants.OP_NOT_STR} ')
        local_expr = local_expr.replace(Constants.OP_AND, f' {Constants.OP_AND_STR} ')
        local_expr = local_expr.replace(Constants.OP_OR, f' {Constants.OP_OR_STR} ')
        local_expr = local_expr.replace(Constants.OP_XOR, f' {Constants.OP_XOR_STR} ')
        local_expr = local_expr.replace(Constants.OP_EQUIV, f' {Constants.OP_EQUIV_STR} ')

        try:
            result = eval(local_expr, {Constants.BUILTINS_KEY: None})
            return bool(result)
        except Exception:
            return self._safe_evaluate(local_expr)

    def _safe_evaluate(self, expr: str) -> bool:
        """Безопасное вычисление без eval"""
        expr = expr.strip()

        if expr.startswith(Constants.PAREN_OPEN) and expr.endswith(Constants.PAREN_CLOSE):
            return self._safe_evaluate(expr[Constants.ONE:-Constants.ONE])

        if expr.startswith(f'{Constants.OP_NOT_STR} '):
            return not self._safe_evaluate(expr[len(Constants.OP_NOT_STR) + Constants.ONE:])

        if f' {Constants.OP_AND_STR} ' in expr:
            parts = expr.split(f' {Constants.OP_AND_STR} ', Constants.ONE)
            return self._safe_evaluate(parts[Constants.ZERO_INDEX]) and \
                   self._safe_evaluate(parts[Constants.FIRST_INDEX])

        if f' {Constants.OP_OR_STR} ' in expr:
            parts = expr.split(f' {Constants.OP_OR_STR} ', Constants.ONE)
            return self._safe_evaluate(parts[Constants.ZERO_INDEX]) or \
                   self._safe_evaluate(parts[Constants.FIRST_INDEX])

        if f' {Constants.OP_XOR_STR} ' in expr:
            parts = expr.split(f' {Constants.OP_XOR_STR} ', Constants.ONE)
            left = self._safe_evaluate(parts[Constants.ZERO_INDEX])
            right = self._safe_evaluate(parts[Constants.FIRST_INDEX])
            return left != right

        if f' {Constants.OP_EQUIV_STR} ' in expr:
            parts = expr.split(f' {Constants.OP_EQUIV_STR} ', Constants.ONE)
            return self._safe_evaluate(parts[Constants.ZERO_INDEX]) == \
                   self._safe_evaluate(parts[Constants.FIRST_INDEX])

        try:
            val = int(expr)
            return bool(val)
        except:
            pass

        return False

    def _generate_truth_table(self):
        """Генерация таблицы истинности"""
        if not self.variables:
            try:
                result = self._parse_expression(self.expression, {})
                self.truth_table = [{Constants.INPUTS_KEY: (),
                                    Constants.OUTPUT_KEY: Constants.ONE if result else Constants.ZERO}]
            except Exception:
                self.truth_table = [{Constants.INPUTS_KEY: (),
                                    Constants.OUTPUT_KEY: Constants.ZERO}]
            return

        self.truth_table = []
        for bits in product([Constants.ZERO, Constants.ONE], repeat=len(self.variables)):
            values = dict(zip(self.variables, bits))
            try:
                result = self._parse_expression(self.expression, values)
                self.truth_table.append({
                    Constants.INPUTS_KEY: bits,
                    Constants.OUTPUT_KEY: Constants.ONE if result else Constants.ZERO
                })
            except Exception as e:
                print(f"Ошибка при вычислении для {values}: {e}")
                self.truth_table.append({
                    Constants.INPUTS_KEY: bits,
                    Constants.OUTPUT_KEY: Constants.ZERO
                })

    def get_truth_table(self) -> list:
        """Получение таблицы истинности"""
        return self.truth_table

    def get_variables(self) -> list:
        """Получение списка переменных"""
        return self.variables

    def get_function_values(self) -> list:
        """Получение значений функции (для СДНФ/СКНФ)"""
        return [row[Constants.OUTPUT_KEY] for row in self.truth_table]

    def print_truth_table(self):
        """Вывод таблицы истинности"""
        if not self.truth_table:
            print("Таблица истинности пуста")
            return

        print("\nТаблица истинности:")
        if self.variables:
            header = Constants.TABLE_HEADER_SEP.join(self.variables) + f" | {Constants.OUTPUT_LABEL}"
            print(header)
            print(Constants.SEPARATOR[:len(header)])

            for row in self.truth_table:
                inputs_str = Constants.TABLE_ROW_SEP.join(str(x) for x in row[Constants.INPUTS_KEY])
                print(f"{inputs_str} | {row[Constants.OUTPUT_KEY]}")
        else:
            print(f"Константная функция: F = {self.truth_table[0][Constants.OUTPUT_KEY]}")