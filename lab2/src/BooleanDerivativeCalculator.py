import re
from itertools import product
from typing import List, Dict, Tuple, Optional, Union
from src.constants import Constants


class BooleanDerivativeCalculator:


    def __init__(self, expression: Union[str, List], variables: List[str]):

        if isinstance(expression, str):
            self.expression = expression
        else:
            self.expression = ""

        self.variables = sorted(variables)
        self.var_to_index = {var: idx for idx, var in enumerate(self.variables)}

        if isinstance(expression, list) and len(expression) > 0 and isinstance(expression[0], dict):
            self.truth_table = self._convert_table_to_dict(expression)
        else:
            self.truth_table = self._build_truth_table()

    def _convert_table_to_dict(self, table: List[dict]) -> Dict[Tuple[int, ...], int]:
        """Преобразование таблицы истинности из формата main.py в словарь"""
        truth_table = {}
        for row in table:
            inputs = row['inputs']
            truth_table[inputs] = row['output']
        return truth_table


    def partial(self, var: str) -> str:
        if var not in self.var_to_index:
            raise ValueError(Constants.format_error(Constants.ERROR_VARIABLE_NOT_FOUND, var=var))

        other_vars = [v for v in self.variables if v != var]
        derivative_values = self._compute_partial_values(var)

        return self._to_expression(derivative_values, other_vars)

    def mixed(self, var1: str, var2: str) -> str:
        if var1 not in self.var_to_index:
            raise ValueError(Constants.format_error(Constants.ERROR_VARIABLE_NOT_FOUND, var=var1))
        if var2 not in self.var_to_index:
            raise ValueError(Constants.format_error(Constants.ERROR_VARIABLE_NOT_FOUND, var=var2))

        if var1 == var2:
            return Constants.DEFAULT_OUTPUT_ZERO

        other_vars = [v for v in self.variables if v not in [var1, var2]]
        derivative_values = self._compute_mixed_values(var1, var2)

        return self._to_expression(derivative_values, other_vars)

    def partial_table(self, var: str) -> List[Tuple[Dict[str, int], int]]:

        if var not in self.var_to_index:
            raise ValueError(Constants.format_error(Constants.ERROR_VARIABLE_NOT_FOUND, var=var))

        other_vars = [v for v in self.variables if v != var]
        other_combinations = self._get_combinations(other_vars)
        derivative_values = self._compute_partial_values(var)

        result = []
        for comb, val in zip(other_combinations, derivative_values):
            result.append((comb, val))

        return result

    def mixed_table(self, var1: str, var2: str) -> List[Tuple[Dict[str, int], int]]:

        if var1 not in self.var_to_index:
            raise ValueError(Constants.format_error(Constants.ERROR_VARIABLE_NOT_FOUND, var=var1))
        if var2 not in self.var_to_index:
            raise ValueError(Constants.format_error(Constants.ERROR_VARIABLE_NOT_FOUND, var=var2))

        other_vars = [v for v in self.variables if v not in [var1, var2]]
        other_combinations = self._get_combinations(other_vars)
        derivative_values = self._compute_mixed_values(var1, var2)

        result = []
        for comb, val in zip(other_combinations, derivative_values):
            result.append((comb, val))

        return result

    def print_partial(self, var: str):
        """Вывод частной производной"""
        if var not in self.var_to_index:
            print(Constants.format_error(Constants.ERROR_VARIABLE_NOT_FOUND, var=var))
            return

        other_vars = [v for v in self.variables if v != var]
        derivative = self.partial(var)
        table = self.partial_table(var)

        print(f"\n∂f/∂{var} = {derivative}")

        if other_vars:
            print(f"\nТаблица истинности:")
            header = " | ".join(other_vars) + f" | ∂f/∂{var}"
            print(f"  {header}")
            print(f"  {'-' * len(header)}")
            for comb, val in table:
                row = " | ".join(str(comb[v]) for v in other_vars)
                print(f"  {row} | {val}")
        else:
            print(f"\nЗначение: {table[0][1]}")

    def print_mixed(self, var1: str, var2: str):
        """Вывод смешанной производной"""
        if var1 not in self.var_to_index or var2 not in self.var_to_index:
            print(f"Ошибка: переменные '{var1}', '{var2}' не найдены")
            return

        derivative = self.mixed(var1, var2)
        table = self.mixed_table(var1, var2)

        print(f"\n∂²f/∂{var1}∂{var2} = {derivative}")

        other_vars = [v for v in self.variables if v not in [var1, var2]]
        if other_vars:
            print(f"\nТаблица истинности:")
            header = " | ".join(other_vars) + f" | ∂²f/∂{var1}∂{var2}"
            print(f"  {header}")
            print(f"  {'-' * len(header)}")
            for comb, val in table:
                row = " | ".join(str(comb[v]) for v in other_vars)
                print(f"  {row} | {val}")
        else:
            print(f"\nЗначение: {table[0][1]}")

    def print_all(self):
        """Вывод всех производных"""
        print(f"\n{Constants.LINE}")
        print(f"Функция: {self.expression if self.expression else 'из таблицы истинности'}")
        print(f"Переменные: {', '.join(self.variables)}")
        print(f"{Constants.LINE}")

        print("\nЧАСТНЫЕ ПРОИЗВОДНЫЕ:")
        for var in self.variables:
            self.print_partial(var)

        if len(self.variables) >= Constants.POWER_BASE:
            print("\nСМЕШАННЫЕ ПРОИЗВОДНЫЕ:")
            for i in range(len(self.variables)):
                for j in range(i + 1, len(self.variables)):
                    self.print_mixed(self.variables[i], self.variables[j])

    def _evaluate(self, expr: str, values: Dict[str, int]) -> int:
        if not expr:
            return 0

        local_expr = expr

        for var, val in values.items():
            local_expr = local_expr.replace(var, str(val))

        while Constants.OP_IMPL in local_expr:
            match = re.search(Constants.OP_IMPL_PATTERN, local_expr)
            if match:
                left, right = match.group(1), match.group(2)
                local_expr = local_expr.replace(match.group(0), f'(~{left}|{right})')
            else:
                break

        local_expr = local_expr.replace(Constants.OP_NOT, f' {Constants.OP_NOT_STR} ')
        local_expr = local_expr.replace(Constants.OP_AND, f' {Constants.OP_AND_STR} ')
        local_expr = local_expr.replace(Constants.OP_OR, f' {Constants.OP_OR_STR} ')
        local_expr = local_expr.replace(Constants.OP_XOR, f' {Constants.OP_XOR_STR} ')
        local_expr = local_expr.replace(Constants.OP_EQUIV, f' {Constants.OP_EQUIV_STR} ')

        local_expr = local_expr.replace('(', ' ( ')
        local_expr = local_expr.replace(')', ' ) ')

        try:
            def xor(x, y):
                return (x and not y) or (not x and y)

            result = eval(local_expr, {'__builtins__': None}, {'xor': xor})
            return 1 if result else 0
        except:
            return self._evaluate_simple(local_expr)

    def _evaluate_simple(self, expr: str) -> int:
        """Упрощенное вычисление без eval"""
        expr = expr.strip()

        # Скобки
        if expr.startswith('(') and expr.endswith(')'):
            return self._evaluate_simple(expr[1:-1])

        # NOT
        if expr.startswith(f'{Constants.OP_NOT_STR} '):
            return 1 - self._evaluate_simple(expr[4:])

        # AND
        if f' {Constants.OP_AND_STR} ' in expr:
            parts = expr.split(f' {Constants.OP_AND_STR} ', 1)
            return self._evaluate_simple(parts[0]) and self._evaluate_simple(parts[1])

        # OR
        if f' {Constants.OP_OR_STR} ' in expr:
            parts = expr.split(f' {Constants.OP_OR_STR} ', 1)
            return self._evaluate_simple(parts[0]) or self._evaluate_simple(parts[1])

        # XOR
        if f' {Constants.OP_XOR_STR} ' in expr:
            parts = expr.split(f' {Constants.OP_XOR_STR} ', 1)
            left = self._evaluate_simple(parts[0])
            right = self._evaluate_simple(parts[1])
            return (left and not right) or (not left and right)

        # EQUIV
        if f' {Constants.OP_EQUIV_STR} ' in expr:
            parts = expr.split(f' {Constants.OP_EQUIV_STR} ', 1)
            return 1 if self._evaluate_simple(parts[0]) == self._evaluate_simple(parts[1]) else 0

        # Число
        try:
            return int(expr)
        except:
            return 0

    def _build_truth_table(self) -> Dict[Tuple[int, ...], int]:
        """Построение таблицы истинности функции"""
        truth_table = {}
        n = len(self.variables)

        for bits in product([0, 1], repeat=n):
            values = dict(zip(self.variables, bits))
            truth_table[bits] = self._evaluate(self.expression, values)

        return truth_table

    def _get_value(self, values: Dict[str, int]) -> int:
        """Получение значения функции для заданных значений переменных"""
        key = tuple(values.get(v, 0) for v in self.variables)
        return self.truth_table.get(key, 0)

    def _get_combinations(self, variables: List[str]) -> List[Dict[str, int]]:
        """Получение всех комбинаций значений для списка переменных"""
        combinations = []
        for bits in product([0, 1], repeat=len(variables)):
            combinations.append(dict(zip(variables, bits)))
        return combinations

    def _compute_partial_values(self, var: str) -> List[int]:
        """Вычисление значений частной производной для всех комбинаций"""
        other_vars = [v for v in self.variables if v != var]
        other_combinations = self._get_combinations(other_vars)

        values = []
        for comb in other_combinations:
            comb0 = {**comb, var: 0}
            comb1 = {**comb, var: 1}
            f0 = self._get_value(comb0)
            f1 = self._get_value(comb1)
            values.append(f1 ^ f0)

        return values

    def _compute_mixed_values(self, var1: str, var2: str) -> List[int]:
        """Вычисление значений смешанной производной для всех комбинаций"""
        other_vars = [v for v in self.variables if v not in [var1, var2]]
        other_combinations = self._get_combinations(other_vars)

        values = []
        for comb in other_combinations:
            f00 = self._get_value({**comb, var1: 0, var2: 0})
            f01 = self._get_value({**comb, var1: 0, var2: 1})
            f10 = self._get_value({**comb, var1: 1, var2: 0})
            f11 = self._get_value({**comb, var1: 1, var2: 1})
            values.append(f00 ^ f01 ^ f10 ^ f11)

        return values

    def _to_expression(self, values: List[int], variables: List[str]) -> str:
        if not variables:
            return str(values[0])

        if all(v == 0 for v in values):
            return Constants.DEFAULT_OUTPUT_ZERO

        if all(v == 1 for v in values):
            return Constants.DEFAULT_OUTPUT_ONE

        combinations = self._get_combinations(variables)
        terms = []

        for comb, val in zip(combinations, values):
            if val == 1:
                term_parts = []
                for var in variables:
                    if comb[var] == 1:
                        term_parts.append(var)
                    else:
                        term_parts.append(f"{Constants.OP_NOT}{var}")
                terms.append(Constants.OP_AND.join(term_parts))

        if not terms:
            return Constants.DEFAULT_OUTPUT_ZERO

        expression = Constants.OP_OR.join(terms)

        expression = expression.replace("(&", "(").replace("&)", ")")

        single_vars = [t for t in terms if Constants.OP_AND not in t and Constants.OP_NOT not in t]
        if len(single_vars) == len(variables) and len(terms) == len(variables):
            return Constants.OP_OR.join(variables)

        common_var = None
        all_have_common = True
        for term in terms:
            term_vars = re.findall(r'[a-z]', term)
            if common_var is None:
                common_var = set(term_vars)
            elif set(term_vars) != common_var:
                all_have_common = False
                break

        if all_have_common and common_var and len(common_var) == 1:
            var = list(common_var)[0]
            return var

        return expression