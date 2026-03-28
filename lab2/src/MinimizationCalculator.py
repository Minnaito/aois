"""Класс для минимизации расчетным методом"""

from src.constants import Constants


class MinimizationCalculator:
    """Минимизатор расчетным методом"""

    def __init__(self, sdnf_terms: list, variables: list):
        self.sdnf_terms = sdnf_terms
        self.variables = variables
        self.n = len(variables)
        self.implicants = []
        self.glue_stages = []
        self.sdnf_result = ""
        self.sknf_result = ""
        self.best_result = ""
        self._minimize()

    def _term_to_binary(self, term_index: int) -> str:
        """Преобразование индекса терма в двоичную строку"""
        return format(term_index, f'0{self.n}b')

    def _term_to_string(self, term_bin: str, for_sdnf: bool = True) -> str:
        """Преобразование двоичного терма в строковое представление"""
        terms = []
        for i, char in enumerate(term_bin):
            if char == Constants.BINARY_ONE:
                if for_sdnf:
                    terms.append(self.variables[i])
                else:
                    terms.append(f"{Constants.OP_NOT}{self.variables[i]}")
            elif char == Constants.BINARY_ZERO:
                if for_sdnf:
                    terms.append(f"{Constants.OP_NOT}{self.variables[i]}")
                else:
                    terms.append(self.variables[i])
        if for_sdnf:
            return " ∧ ".join(terms) if terms else Constants.DEFAULT_OUTPUT_ONE
        else:
            return " ∨ ".join(terms) if terms else Constants.DEFAULT_OUTPUT_ZERO

    def _can_glue(self, term1: str, term2: str) -> bool:
        """Проверка возможности склеивания двух термов"""
        diff_count = 0

        for i in range(self.n):
            if term1[i] != term2[i]:
                diff_count += 1

        return diff_count == 1

    def _glue_terms(self, term1: str, term2: str) -> str:
        """Склеивание двух термов"""
        result = []
        for i in range(self.n):
            if term1[i] == term2[i]:
                result.append(term1[i])
            else:
                result.append(Constants.BINARY_X)
        return ''.join(result)

    def _get_implicant_string(self, implicant: str, for_sdnf: bool = True) -> str:
        """Преобразование импликанты в строковое представление"""
        terms = []
        for i, char in enumerate(implicant):
            if char == Constants.BINARY_ONE:
                if for_sdnf:
                    terms.append(self.variables[i])
                else:
                    terms.append(f"{Constants.OP_NOT}{self.variables[i]}")
            elif char == Constants.BINARY_ZERO:
                if for_sdnf:
                    terms.append(f"{Constants.OP_NOT}{self.variables[i]}")
                else:
                    terms.append(self.variables[i])

        if for_sdnf:
            return " ∧ ".join(terms) if terms else Constants.DEFAULT_OUTPUT_ONE
        else:
            return " ∨ ".join(terms) if terms else Constants.DEFAULT_OUTPUT_ZERO

    def _minimize_sdnf(self):
        """Минимизация по СДНФ (по единицам)"""
        print("\n" + Constants.LINE[:50])
        print("    МИНИМИЗАЦИЯ ПО СДНФ (по единицам)")
        print(Constants.LINE[:50])

        if not self.sdnf_terms:
            print("Функция тождественно равна 0")
            self.sdnf_result = Constants.DEFAULT_OUTPUT_ZERO
            return

        current_terms = [self._term_to_binary(idx) for idx in self.sdnf_terms]

        initial_terms = [self._term_to_string(term) for term in current_terms]
        print(f"Исходная СДНФ: {' ∨ '.join(['(' + term + ')' for term in initial_terms])}")

        stage_num = 1
        self.implicants = []
        glue_stages = []

        while len(current_terms) > 0:
            new_terms = []
            used = [False] * len(current_terms)

            for i in range(len(current_terms)):
                for j in range(i + 1, len(current_terms)):
                    if self._can_glue(current_terms[i], current_terms[j]):
                        glued = self._glue_terms(current_terms[i], current_terms[j])
                        if glued not in new_terms:
                            new_terms.append(glued)
                        used[i] = True
                        used[j] = True

            for i, term in enumerate(current_terms):
                if not used[i] and term not in self.implicants:
                    self.implicants.append(term)

            if new_terms:
                new_terms_str = []
                for term in new_terms:
                    term_str = self._get_implicant_string(term)
                    new_terms_str.append(term_str)
                print(f"Этап склеивания {stage_num}: {' ∨ '.join(['(' + t + ')' for t in new_terms_str])}")
                stage_num += 1

            current_terms = new_terms

        if self.implicants:
            prime_implicants = [self._get_implicant_string(imp) for imp in self.implicants]
            print(f"Все простые импликанты: {' ∨ '.join(['(' + t + ')' for t in prime_implicants])}")

            self._remove_redundant_implicants()

            essential_implicants = [self._get_implicant_string(imp) for imp in self.implicants]
            print(f"Существенные импликанты: {' ∨ '.join(['(' + t + ')' for t in essential_implicants])}")
            self.sdnf_result = ' ∨ '.join(['(' + t + ')' for t in essential_implicants])
        else:
            self.sdnf_result = Constants.DEFAULT_OUTPUT_ZERO

        print(f"Результат минимизации по СДНФ: {self.sdnf_result}")

    def _minimize_sknf(self):
        """Минимизация по СКНФ (по нулям)"""
        print("\n" + Constants.LINE[:50])
        print("    МИНИМИЗАЦИЯ ПО СКНФ (по нулям)")
        print(Constants.LINE[:50])

        all_indices = set(range(Constants.POWER_BASE ** self.n))
        ones_indices = set(self.sdnf_terms)
        zeros_indices = sorted(all_indices - ones_indices)

        if not zeros_indices:
            print("Функция тождественно равна 1")
            self.sknf_result = Constants.DEFAULT_OUTPUT_ONE
            return

        current_terms = [self._term_to_binary(idx) for idx in zeros_indices]

        initial_terms = [self._term_to_string(term, for_sdnf=False) for term in current_terms]
        print(f"Исходная СКНФ: {' ∧ '.join(['(' + term + ')' for term in initial_terms])}")

        stage_num = 1
        sknf_implicants = []

        working_terms = current_terms.copy()

        while len(working_terms) > 0:
            new_terms = []
            used = [False] * len(working_terms)

            for i in range(len(working_terms)):
                for j in range(i + 1, len(working_terms)):
                    if self._can_glue(working_terms[i], working_terms[j]):
                        glued = self._glue_terms(working_terms[i], working_terms[j])
                        if glued not in new_terms:
                            new_terms.append(glued)
                        used[i] = True
                        used[j] = True

            for i, term in enumerate(working_terms):
                if not used[i] and term not in sknf_implicants:
                    sknf_implicants.append(term)

            if new_terms:
                new_terms_str = []
                for term in new_terms:
                    term_str = self._get_implicant_string(term, for_sdnf=False)
                    new_terms_str.append(term_str)
                print(f"Этап склеивания {stage_num}: {' ∧ '.join(['(' + t + ')' for t in new_terms_str])}")
                stage_num += 1

            working_terms = new_terms

        if len(sknf_implicants) == 1 and sknf_implicants[0].count(Constants.BINARY_X) == self.n:
            print("СКНФ уже минимальна (состоит из одного терма)")
            result_terms = [self._get_implicant_string(imp, for_sdnf=False) for imp in sknf_implicants]
            self.sknf_result = ' ∧ '.join(['(' + t + ')' for t in result_terms])
        else:
            essential = []
            for i, imp in enumerate(sknf_implicants):
                is_essential = False
                for term in zeros_indices:
                    term_bin = self._term_to_binary(term)
                    if self._covers(imp, term_bin):
                        covered_by_other = False
                        for j, other_imp in enumerate(sknf_implicants):
                            if i != j and self._covers(other_imp, term_bin):
                                covered_by_other = True
                                break
                        if not covered_by_other:
                            is_essential = True
                            break
                if is_essential:
                    essential.append(imp)

            sknf_implicants = essential if essential else sknf_implicants
            result_terms = [self._get_implicant_string(imp, for_sdnf=False) for imp in sknf_implicants]
            self.sknf_result = ' ∧ '.join(['(' + t + ')' for t in result_terms])

        print(f"Результат минимизации по СКНФ: {self.sknf_result}")

    def _remove_redundant_implicants(self):
        """Удаление лишних импликант"""
        essential = []

        for i, imp in enumerate(self.implicants):
            is_essential = False

            for term in self.sdnf_terms:
                term_bin = self._term_to_binary(term)
                if self._covers(imp, term_bin):
                    covered_by_other = False
                    for j, other_imp in enumerate(self.implicants):
                        if i != j and self._covers(other_imp, term_bin):
                            covered_by_other = True
                            break
                    if not covered_by_other:
                        is_essential = True
                        break

            if is_essential:
                essential.append(imp)

        self.implicants = essential if essential else self.implicants

    def _covers(self, implicant: str, term: str) -> bool:
        """Проверка, покрывает ли импликанта терм"""
        for i in range(self.n):
            if implicant[i] != Constants.BINARY_X and implicant[i] != term[i]:
                return False
        return True

    def _minimize(self):
        """Минимизация расчетным методом"""
        self._minimize_sdnf()
        self._minimize_sknf()

        print("\n" + Constants.LINE[:50])
        print("    Лучший результат")
        print(Constants.LINE[:50])

        sdnf_len = len(self.sdnf_result.replace(' ', ''))
        sknf_len = len(self.sknf_result.replace(' ', ''))

        if sdnf_len <= sknf_len:
            self.best_result = self.sdnf_result
            print(f"Лучший результат (по СДНФ): {self.best_result}")
        else:
            self.best_result = self.sknf_result
            print(f"Лучший результат (по СКНФ): {self.best_result}")

    def get_minimized_function(self) -> str:
        """Получение минимизированной функции"""
        return self.best_result

    def print_result(self):
        """Вывод результата минимизации"""
        print(f"\nРезультат: {self.best_result}")