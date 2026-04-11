"""Класс для построения полинома Жегалкина"""

from src.constants import Constants


class ZhegalkinPolynomialBuilder:
    """Построитель полинома Жегалкина"""

    def __init__(self, truth_table: list, variables: list):
        self.truth_table = truth_table
        self.variables = variables[::-1]
        self.polynomial = ""
        self._build_polynomial()

    def _build_polynomial(self):
        n = len(self.variables)
        size = Constants.POWER_BASE ** n
        values = [row[Constants.OUTPUT_KEY] for row in self.truth_table]

        coefficients = values.copy()
        for i in range(n):
            step = Constants.POWER_BASE ** i
            for j in range(size):
                if j & (Constants.POWER_BASE ** i):
                    coefficients[j] ^= coefficients[j ^ (Constants.POWER_BASE ** i)]

        terms = []
        for mask in range(size):
            if coefficients[mask] == Constants.ONE:
                term = self._build_term(mask)
                if term:
                    terms.append(term)

        if not terms:
            self.polynomial = Constants.DEFAULT_OUTPUT_ZERO
        else:
            self.polynomial = f" {Constants.OP_XOR} ".join(terms)

        def term_key(term):
            if term == Constants.DEFAULT_OUTPUT_ONE:
                return Constants.ZERO
            return len(term)

        terms.sort(key=term_key)

        if not terms:
            self.polynomial = Constants.DEFAULT_OUTPUT_ZERO
        else:
            self.polynomial = f" {Constants.OP_XOR} ".join(terms)

    def _build_term(self, mask: int) -> str:
        """Построение терма по маске"""
        if mask == Constants.ZERO:
            return Constants.DEFAULT_OUTPUT_ONE

        terms = []
        n = len(self.variables)
        for i in range(n - Constants.ONE, -Constants.ONE, -Constants.ONE):
            if mask & (Constants.POWER_BASE ** i):
                terms.append(self.variables[i])

        if len(terms) == Constants.ONE:
            return terms[Constants.ZERO_INDEX]

        return ''.join(terms)

    def get_polynomial(self) -> str:
        """Возвращает полином Жегалкина"""
        return self.polynomial

    def print_polynomial(self):
        """Выводит полином Жегалкина"""
        print(f"Полином Жегалкина: {self.polynomial}")
