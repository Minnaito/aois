"""Класс для минимизации расчетно-табличным методом"""

from src.constants import Constants


class MinimizationTabular:
    """Минимизатор расчетно-табличным методом"""

    def __init__(self, sdnf_terms: list, variables: list):
        self.sdnf_terms = sdnf_terms
        self.variables = variables
        self.n = len(variables)
        self.implicants = []
        self.table = []
        self.minimized_function = ""
        self._minimize()

    def _term_to_binary(self, term_index: int) -> str:
        """Преобразование индекса терма в двоичную строку"""
        return format(term_index, f'0{self.n}{Constants.BINARY_FORMAT_SPEC}')

    def _can_glue(self, term1: str, term2: str) -> bool:
        """Проверка возможности склеивания"""
        diff_count = 0
        for i in range(self.n):
            if term1[i] != term2[i]:
                diff_count += Constants.ONE
        return diff_count == Constants.GLUE_DIFF_COUNT

    def _glue_terms(self, term1: str, term2: str) -> str:
        """Склеивание термов"""
        result = []
        for i in range(self.n):
            if term1[i] == term2[i]:
                result.append(term1[i])
            else:
                result.append(Constants.BINARY_X)
        return ''.join(result)

    def _get_implicant_string(self, implicant: str) -> str:
        """Преобразование импликанты в строку"""
        terms = []
        for i, char in enumerate(implicant):
            if char == Constants.BINARY_ONE:
                terms.append(self.variables[i])
            elif char == Constants.BINARY_ZERO:
                terms.append(f"{Constants.OP_NOT}{self.variables[i]}")
        return f" {Constants.OP_AND} ".join(terms) if terms else Constants.DEFAULT_OUTPUT_ONE

    def _covers(self, implicant: str, term: str) -> bool:
        """Проверка покрытия"""
        for i in range(self.n):
            if implicant[i] != Constants.BINARY_X and implicant[i] != term[i]:
                return False
        return True

    def _build_implicants(self):
        """Построение всех простых импликант"""
        if not self.sdnf_terms:
            self.implicants = []
            return

        current_terms = [self._term_to_binary(idx) for idx in self.sdnf_terms]
        all_implicants = []

        iteration = Constants.ZERO
        max_iterations = Constants.MAX_GLUE_ITERATIONS

        while len(current_terms) > Constants.ZERO and iteration < max_iterations:
            new_terms = []
            used = [False] * len(current_terms)

            for i in range(len(current_terms)):
                for j in range(i + Constants.ONE, len(current_terms)):
                    if self._can_glue(current_terms[i], current_terms[j]):
                        glued = self._glue_terms(current_terms[i], current_terms[j])
                        if glued not in new_terms:
                            new_terms.append(glued)
                        used[i] = True
                        used[j] = True

            for i, term in enumerate(current_terms):
                if not used[i] and term not in all_implicants:
                    all_implicants.append(term)

            current_terms = new_terms
            iteration += Constants.ONE

        self.implicants = all_implicants

    def _build_table(self):
        """Построение таблицы покрытий"""
        if not self.implicants or not self.sdnf_terms:
            self.table = []
            return

        term_strings = [self._term_to_binary(idx) for idx in self.sdnf_terms]

        self.table = []
        for imp in self.implicants:
            row = []
            for term in term_strings:
                row.append(self._covers(imp, term))
            self.table.append(row)

    def _find_essential_implicants(self):
        """Поиск существенных импликант"""
        if not self.table or not self.implicants:
            return []

        essential = []
        term_strings = [self._term_to_binary(idx) for idx in self.sdnf_terms]

        for j, term in enumerate(term_strings):
            covering = []
            for i, imp in enumerate(self.implicants):
                if self.table[i][j]:
                    covering.append(i)

            if len(covering) == Constants.SINGLE_COVER:
                essential.append(self.implicants[covering[Constants.ZERO_INDEX]])

        essential = list(dict.fromkeys(essential))
        return essential

    def _remove_redundant_implicants(self, essential):
        """Удаление лишних импликант"""
        if not self.implicants:
            return []

        term_strings = [self._term_to_binary(idx) for idx in self.sdnf_terms]

        covered_terms = set()
        for imp in essential:
            for j, term in enumerate(term_strings):
                if self._covers(imp, term):
                    covered_terms.add(j)

        remaining = set(range(len(term_strings))) - covered_terms

        if remaining:
            remaining_implicants = []
            for imp in self.implicants:
                if imp not in essential:
                    cover_count = sum(Constants.ONE for j in remaining if self._covers(imp, term_strings[j]))
                    if cover_count > Constants.ZERO:
                        remaining_implicants.append((imp, cover_count))

            remaining_implicants.sort(key=lambda x: x[Constants.SECOND_INDEX], reverse=True)

            for imp, _ in remaining_implicants:
                if remaining:
                    new_covered = set()
                    for j in remaining:
                        if self._covers(imp, term_strings[j]):
                            new_covered.add(j)

                    if new_covered:
                        essential.append(imp)
                        remaining -= new_covered

        return essential

    def _minimize(self):
        """Минимизация расчетно-табличным методом"""
        if not self.sdnf_terms:
            self.minimized_function = Constants.DEFAULT_OUTPUT_ZERO
            return

        self._build_implicants()

        if not self.implicants:
            self.minimized_function = Constants.DEFAULT_OUTPUT_ZERO
            return

        self._build_table()

        essential = self._find_essential_implicants()

        final_implicants = self._remove_redundant_implicants(essential)

        if final_implicants:
            terms = [self._get_implicant_string(imp) for imp in final_implicants]
            self.minimized_function = f" {Constants.OP_OR} ".join([f'({t})' for t in terms])
        else:
            self.minimized_function = Constants.DEFAULT_OUTPUT_ZERO

    def get_minimized_function(self) -> str:
        """Получение минимизированной функции"""
        return self.minimized_function

    def print_table(self):
        """Вывод таблицы покрытий"""
        if not self.table or not self.implicants or not self.sdnf_terms:
            print("\nТаблица покрытий пуста")
            return

        term_strings = [self._term_to_binary(idx) for idx in self.sdnf_terms]

        print("\n" + Constants.LINE)
        print("ТАБЛИЦА ПОКРЫТИЙ")
        print(Constants.LINE)

        header = "Импликанта"
        for i, term in enumerate(term_strings):
            header += f" | {term}"
        print(header)
        print(Constants.SEPARATOR[:len(header)])

        for i, imp in enumerate(self.implicants):
            imp_str = self._get_implicant_string(imp)
            row = f"{imp_str:^10}"
            for j in range(len(term_strings)):
                if self.table[i][j]:
                    row += f" |   {Constants.TABLE_COVER_MARK}   "
                else:
                    row += f" |       "
            print(row)

        print(Constants.LINE)

    def print_result(self):
        """Вывод результата"""
        print(f"\nРезультат минимизации: {self.minimized_function}")
        self.print_table()