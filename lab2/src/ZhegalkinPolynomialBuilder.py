"""Класс для построения полинома Жегалкина"""

from src.constants import Constants


class ZhegalkinPolynomialBuilder:
    """Построитель полинома Жегалкина"""

    def __init__(self, truth_table: list, variables: list):
        self.truth_table = truth_table
        self.variables = variables
        self.polynomial = ""
        self._build_polynomial()

    def _build_polynomial(self):
        """Построение полинома Жегалкина"""
        n = len(self.variables)
        size = 1 << n
        values = [row['output'] for row in self.truth_table]

        coefficients = values.copy()

        for i in range(n):
            step = 1 << i
            for j in range(size):
                if j & (1 << i):
                    coefficients[j] ^= coefficients[j ^ (1 << i)]

        terms = []
        for mask in range(size):
            if coefficients[mask] == 1:
                term = self._build_term(mask)
                if term:
                    terms.append(term)

        def term_key(term):
            if term == Constants.DEFAULT_OUTPUT_ONE:
                return 0
            return len(term.split(Constants.OP_AND))

        terms.sort(key=term_key)

        if not terms:
            self.polynomial = Constants.DEFAULT_OUTPUT_ZERO
        else:
            self.polynomial = " ⊕ ".join(terms)

    def _build_term(self, mask: int) -> str:
        """Построение терма по маске"""
        if mask == 0:
            return Constants.DEFAULT_OUTPUT_ONE

        terms = []
        for i, var in enumerate(self.variables):
            if mask & (1 << i):
                terms.append(var)

        if len(terms) == 1:
            return terms[0]

        return Constants.OP_AND.join(terms)

        def term_key(term):
            if term == Constants.DEFAULT_OUTPUT_ONE:
                return 0
            return len(term.split(Constants.OP_AND))

        terms.sort(key=term_key)

        self.polynomial = " ⊕ ".join(terms) if terms else Constants.DEFAULT_OUTPUT_ZERO

    def get_polynomial(self) -> str:
        """Получение полинома Жегалкина"""
        return self.polynomial

    def print_polynomial(self):
        """Вывод полинома Жегалкина"""
        print(f"\nПолином Жегалкина: {self.polynomial}")