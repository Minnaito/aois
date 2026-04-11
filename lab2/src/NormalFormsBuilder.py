"""Класс для построения СДНФ и СКНФ"""

from src.constants import Constants


class NormalFormsBuilder:
    """Построитель совершенных нормальных форм"""

    def __init__(self, truth_table: list, variables: list):
        self.truth_table = truth_table
        self.variables = sorted(variables)
        self.sdnf = ""
        self.sknf = ""
        self.numeric_sdnf = []
        self.numeric_sknf = []
        self.index_form = ""
        self._build_forms()

    def _build_sdnf_term(self, inputs: tuple) -> str:
        """Построение терма для СДНФ"""
        if not self.variables:
            return Constants.DEFAULT_OUTPUT_ONE

        terms = []
        for i, var in enumerate(self.variables):
            if i < len(inputs):
                if inputs[i] == Constants.ONE:
                    terms.append(var)
                else:
                    terms.append(f"{Constants.OP_NOT}{var}")
            else:
                terms.append(var)

        if len(terms) == Constants.ONE:
            return terms[Constants.ZERO_INDEX]

        return f"{Constants.PAREN_OPEN}{f' {Constants.OP_AND_SYMBOL} '.join(terms)}{Constants.PAREN_CLOSE}"

    def _build_sknf_term(self, inputs: tuple) -> str:
        """Построение терма для СКНФ"""
        if not self.variables:
            return Constants.DEFAULT_OUTPUT_ZERO

        terms = []
        for i, var in enumerate(self.variables):
            if i < len(inputs):
                if inputs[i] == Constants.ZERO:
                    terms.append(var)
                else:
                    terms.append(f"{Constants.OP_NOT}{var}")
            else:
                terms.append(var)

        if len(terms) == Constants.ONE:
            return terms[Constants.ZERO_INDEX]

        return f"{Constants.PAREN_OPEN}{f' {Constants.OP_OR_SYMBOL} '.join(terms)}{Constants.PAREN_CLOSE}"

    def _build_forms(self):
        """Построение СДНФ и СКНФ"""
        sdnf_terms = []
        sknf_terms = []
        self.numeric_sdnf = []
        self.numeric_sknf = []

        n = len(self.variables)

        for idx, row in enumerate(self.truth_table):
            if Constants.INPUTS_KEY in row:
                inputs = row[Constants.INPUTS_KEY]
            else:
                inputs = self._get_inputs_from_index(idx, n)

            output = row[Constants.OUTPUT_KEY]

            if output == Constants.ONE:
                self.numeric_sdnf.append(idx)
                term = self._build_sdnf_term(inputs)
                sdnf_terms.append(term)
            else:
                self.numeric_sknf.append(idx)
                term = self._build_sknf_term(inputs)
                sknf_terms.append(term)

        if sdnf_terms:
            unique_terms = list(dict.fromkeys(sdnf_terms))
            formatted_sdnf = []
            for term in unique_terms:
                if term.startswith(Constants.PAREN_OPEN) and term.endswith(Constants.PAREN_CLOSE):
                    inner = term[Constants.FIRST_INDEX:-Constants.FIRST_INDEX]
                    if f' {Constants.OP_AND_SYMBOL} ' in inner:
                        formatted_sdnf.append(term)
                    else:
                        formatted_sdnf.append(inner)
                else:
                    formatted_sdnf.append(term)
            self.sdnf = f" {Constants.OP_OR_SYMBOL} ".join(formatted_sdnf)
        else:
            self.sdnf = Constants.DEFAULT_OUTPUT_ZERO

        # СКНФ
        if sknf_terms:
            unique_terms = list(dict.fromkeys(sknf_terms))
            formatted_sknf = []
            for term in unique_terms:
                if term.startswith(Constants.PAREN_OPEN) and term.endswith(Constants.PAREN_CLOSE):
                    inner = term[Constants.FIRST_INDEX:-Constants.FIRST_INDEX]
                    if f' {Constants.OP_OR_SYMBOL} ' in inner:
                        formatted_sknf.append(term)
                    else:
                        formatted_sknf.append(inner)
                else:
                    formatted_sknf.append(term)
            self.sknf = f" {Constants.OP_AND_SYMBOL} ".join(formatted_sknf)
        else:
            self.sknf = Constants.DEFAULT_OUTPUT_ONE

        self.index_form = self._build_index_form()

    def _get_inputs_from_index(self, idx: int, n: int) -> tuple:
        """Восстановление входных значений по индексу"""
        if n == Constants.ZERO:
            return ()
        inputs = []
        for i in range(n - Constants.ONE, -Constants.ONE, -Constants.ONE):
            inputs.append((idx >> i) & Constants.ONE)
        return tuple(inputs)

    def _build_index_form(self) -> str:
        """Построение индексной формы функции (вектор функции)"""
        values = [str(row[Constants.OUTPUT_KEY]) for row in self.truth_table]
        return "".join(values)

    def get_sdnf(self) -> str:
        """Получение СДНФ"""
        return self.sdnf

    def get_sknf(self) -> str:
        """Получение СКНФ"""
        return self.sknf

    def get_numeric_forms(self) -> tuple:
        """Получение числовых форм"""
        return list(self.numeric_sdnf), list(self.numeric_sknf)

    def get_index_form(self) -> str:
        """Получение индексной формы"""
        return self.index_form

    def print_forms(self):
        """Вывод форм"""
        print(f"\nСДНФ: {self.sdnf}")
        if self.numeric_sdnf:
            print(f"Числовая форма СДНФ: {list(self.numeric_sdnf)}")
        else:
            print("Числовая форма СДНФ: []")

        print(f"\nСКНФ: {self.sknf}")
        if self.numeric_sknf:
            print(f"Числовая форма СКНФ: {list(self.numeric_sknf)}")
        else:
            print("Числовая форма СКНФ: []")

        print(f"\nВектор функции: {self.index_form}")
