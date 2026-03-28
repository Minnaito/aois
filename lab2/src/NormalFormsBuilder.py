"""Класс для построения СДНФ и СКНФ"""

from src.constants import Constants


class NormalFormsBuilder:
    """Построитель совершенных нормальных форм"""

    def __init__(self, truth_table: list, variables: list):
        self.truth_table = truth_table
        self.variables = variables
        self.sdnf = ""
        self.sknf = ""
        self.numeric_sdnf = []
        self.numeric_sknf = []
        self.index_form = ""
        self._build_forms()

    def _build_forms(self):
        """Построение СДНФ и СКНФ"""
        sdnf_terms = []
        sknf_terms = []
        self.numeric_sdnf = []
        self.numeric_sknf = []

        for idx, row in enumerate(self.truth_table):
            if row['output'] == 1:
                self.numeric_sdnf.append(idx)
                term = self._build_sdnf_term(row['inputs'])
                sdnf_terms.append(term)
            else:
                self.numeric_sknf.append(idx)
                term = self._build_sknf_term(row['inputs'])
                sknf_terms.append(term)

        self.sdnf = " ∨ ".join(sdnf_terms) if sdnf_terms else Constants.DEFAULT_OUTPUT_ZERO
        self.sknf = " ∧ ".join(sknf_terms) if sknf_terms else Constants.DEFAULT_OUTPUT_ONE

        self.index_form = self._build_index_form()

    def _build_sdnf_term(self, inputs: tuple) -> str:
        """Построение терма для СДНФ"""
        terms = []
        for var, val in zip(self.variables, inputs):
            if val == 1:
                terms.append(var)
            else:
                terms.append(f"{Constants.OP_NOT}{var}")
        return "(" + " ∧ ".join(terms) + ")"

    def _build_sknf_term(self, inputs: tuple) -> str:
        """Построение терма для СКНФ"""
        terms = []
        for var, val in zip(self.variables, inputs):
            if val == 0:
                terms.append(var)
            else:
                terms.append(f"{Constants.OP_NOT}{var}")
        return "(" + " ∨ ".join(terms) + ")"

    def _build_index_form(self) -> str:
        """Построение индексной формы функции"""
        values = [str(row['output']) for row in self.truth_table]
        binary = "".join(values)
        decimal = int(binary, Constants.POWER_BASE)
        return f"{binary} ({decimal})"

    def get_sdnf(self) -> str:
        """Получение СДНФ"""
        return self.sdnf

    def get_sknf(self) -> str:
        """Получение СКНФ"""
        return self.sknf

    def get_numeric_forms(self) -> tuple:
        """Получение числовых форм"""
        return self.numeric_sdnf, self.numeric_sknf

    def get_index_form(self) -> str:
        """Получение индексной формы"""
        return self.index_form

    def print_forms(self):
        """Вывод форм"""
        print(f"\nСДНФ: {self.sdnf}")
        print(f"Числовая форма СДНФ: {self.numeric_sdnf}")
        print(f"\nСКНФ: {self.sknf}")
        print(f"Числовая форма СКНФ: {self.numeric_sknf}")
        print(f"\nИндексная форма: {self.index_form}")