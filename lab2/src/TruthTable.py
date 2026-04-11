from typing import List, Tuple, Dict, Iterator
from itertools import product
from .ExpressionParser import BooleanExpressionParser
from src.constants import Constants


class TruthTable:
    """Модель таблицы истинности"""

    def __init__(self, variables: List[str], expression: str, parser: BooleanExpressionParser):
        self.variables = variables
        self.expression = expression
        self.parser = parser
        self._table = self._build()

    def _build(self) -> List[Tuple[Tuple[int, ...], int]]:
        """Построение таблицы истинности"""
        table = []
        n = len(self.variables)

        if n == Constants.ZERO:
            if self.expression == Constants.DEFAULT_OUTPUT_ZERO:
                table = [((), Constants.ZERO)]
            elif self.expression == Constants.DEFAULT_OUTPUT_ONE:
                table = [((), Constants.ONE)]
            return table

        for bits in product([Constants.ZERO, Constants.ONE], repeat=n):
            values = dict(zip(self.variables, bits))
            result = self.parser.evaluate(self.expression, values)
            table.append((bits, result))

        return table

    def get_table(self) -> List[Tuple[Tuple[int, ...], int]]:
        """Получить таблицу истинности"""
        return self._table.copy()

    def get_rows(self) -> Iterator[Tuple[Tuple[int, ...], int]]:
        """Итератор по строкам таблицы"""
        yield from self._table

    def get_result_column(self) -> List[int]:
        """Получить столбец результатов"""
        return [result for _, result in self._table]

    def get_ones_indices(self) -> List[int]:
        """Получить индексы наборов, где результат = 1"""
        return [i for i, (_, result) in enumerate(self._table) if result == Constants.ONE]

    def get_zeros_indices(self) -> List[int]:
        """Получить индексы наборов, где результат = 0"""
        return [i for i, (_, result) in enumerate(self._table) if result == Constants.ZERO]

    def get_ones_sets(self) -> List[Tuple[int, ...]]:
        """Получить наборы, где результат = 1"""
        return [bits for bits, result in self._table if result == Constants.ONE]

    def get_zeros_sets(self) -> List[Tuple[int, ...]]:
        """Получить наборы, где результат = 0"""
        return [bits for bits, result in self._table if result == Constants.ZERO]

    def get_value_at(self, bits: Tuple[int, ...]) -> int:
        """Получить значение для конкретного набора"""
        for b, result in self._table:
            if b == bits:
                return result
        raise ValueError(f"Набор {bits} не найден")

    def __len__(self) -> int:
        return len(self._table)

    def __iter__(self):
        return iter(self._table)
