from src.constants import Constants


class MinimizationTabular:
    """Класс для минимизации расчетно-табличным методом (Мак-Класки)"""

    def __init__(self, indices, variables, is_sdnf=True):
        self.indices = sorted(indices)
        self.variables = variables
        self.n = len(variables)
        self.is_sdnf = is_sdnf

        if not self.indices:
            self.result = Constants.DEFAULT_OUTPUT_ZERO if self.is_sdnf else Constants.DEFAULT_OUTPUT_ONE
            self.prime_implicants = []
            self.coverage_table = []
            return

        if len(self.indices) == Constants.POWER_BASE ** self.n:
            self.result = Constants.DEFAULT_OUTPUT_ONE if self.is_sdnf else Constants.DEFAULT_OUTPUT_ZERO
            self.prime_implicants = []
            self.coverage_table = []
            return

        self.prime_implicants = self._find_prime_implicants()

        self.result = self._minimize()

    def _to_binary(self, num, length=None):
        """Преобразование числа в двоичную строку"""
        if length is None:
            length = self.n
        return format(num, f'0{length}b')

    def _count_ones(self, binary_str):
        """Подсчет количества единиц в двоичной строке"""
        return binary_str.count(Constants.BINARY_ONE)

    def _count_zeros(self, binary_str):
        """Подсчет количества нулей в двоичной строке"""
        return binary_str.count(Constants.BINARY_ZERO)

    def _combine(self, term1, term2):
        """Склеивание двух термов"""
        diff_pos = -Constants.ONE
        for i in range(len(term1)):
            if term1[i] != term2[i]:
                if diff_pos == -Constants.ONE:
                    diff_pos = i
                else:
                    return None
        if diff_pos != -Constants.ONE:
            return term1[:diff_pos] + Constants.BINARY_X + term1[diff_pos + Constants.ONE:]
        return None

    def _find_prime_implicants(self):
        """Нахождение всех простых импликант/имплицент методом Мак-Класки"""
        if not self.indices:
            return []

        terms = [self._to_binary(idx) for idx in self.indices]

        groups = {}
        for term in terms:
            if self.is_sdnf:
                count = self._count_ones(term)
            else:
                count = self._count_zeros(term)
            if count not in groups:
                groups[count] = []
            groups[count].append(term)

        used = set()
        prime_implicants = []

        while True:
            new_groups = {}
            new_used = set()

            sorted_keys = sorted(groups.keys())

            for i in range(len(sorted_keys) - Constants.ONE):
                key1 = sorted_keys[i]
                key2 = sorted_keys[i + Constants.ONE]

                if key2 - key1 != Constants.ONE:
                    continue

                for term1 in groups[key1]:
                    for term2 in groups[key2]:
                        combined = self._combine(term1, term2)
                        if combined:
                            new_used.add(term1)
                            new_used.add(term2)
                            if self.is_sdnf:
                                count = self._count_ones(combined.replace(Constants.BINARY_X, ''))
                            else:
                                count = self._count_zeros(combined.replace(Constants.BINARY_X, ''))
                            if count not in new_groups:
                                new_groups[count] = []
                            if combined not in new_groups[count]:
                                new_groups[count].append(combined)

            for key in groups:
                for term in groups[key]:
                    if term not in new_used and term not in prime_implicants:
                        prime_implicants.append(term)

            if not new_groups:
                break

            groups = new_groups

        prime_implicants = list(dict.fromkeys(prime_implicants))

        return prime_implicants

    def _term_to_expression(self, term):
        """Преобразование терма (например, '10-1') в логическое выражение"""
        if not term:
            return ""

        parts = []
        for i, char in enumerate(term):
            if char == Constants.BINARY_X:
                continue
            var = self.variables[i]
            if self.is_sdnf:
                if char == Constants.BINARY_ZERO:
                    parts.append(f"{Constants.OP_NOT}{var}")
                else:
                    parts.append(var)
            else:
                if char == Constants.BINARY_ZERO:
                    parts.append(var)
                else:
                    parts.append(f"{Constants.OP_NOT}{var}")

        if not parts:
            return Constants.DEFAULT_OUTPUT_ONE if self.is_sdnf else Constants.DEFAULT_OUTPUT_ZERO

        if self.is_sdnf:
            if len(parts) == Constants.ONE:
                return parts[Constants.ZERO_INDEX]
            return f" {Constants.OP_AND_SYMBOL} ".join(parts)
        else:
            if len(parts) == Constants.ONE:
                return parts[Constants.ZERO_INDEX]
            return f" {Constants.OP_OR_SYMBOL} ".join(parts)

    def _covers(self, implicant, index):
        """Проверяет, покрывает ли импликанта данный индекс"""
        binary = self._to_binary(index)
        for i in range(len(implicant)):
            if implicant[i] != Constants.BINARY_X and implicant[i] != binary[i]:
                return False
        return True

    def _minimize(self):
        """Находит минимальное покрытие"""
        if not self.prime_implicants:
            return Constants.DEFAULT_OUTPUT_ZERO if self.is_sdnf else Constants.DEFAULT_OUTPUT_ONE

        table = []
        for imp in self.prime_implicants:
            row = []
            for idx in self.indices:
                row.append(self._covers(imp, idx))
            table.append(row)

        essential = set()
        for j in range(len(self.indices)):
            covering_imps = [i for i in range(len(self.prime_implicants)) if table[i][j]]
            if len(covering_imps) == Constants.ONE:
                essential.add(covering_imps[Constants.ZERO_INDEX])

        covered_indices = set()
        for i in essential:
            for j in range(len(self.indices)):
                if table[i][j]:
                    covered_indices.add(j)

        remaining_indices = [j for j in range(len(self.indices)) if j not in covered_indices]

        if remaining_indices:
            remaining_imps = [i for i in range(len(self.prime_implicants)) if i not in essential]

            remaining_table = []
            for i in remaining_imps:
                row = []
                for j in remaining_indices:
                    row.append(table[i][j])
                remaining_table.append(row)

            uncovered = set(range(len(remaining_indices)))
            selected = []

            while uncovered:
                best_imp = -Constants.ONE
                best_count = Constants.ZERO
                for i in range(len(remaining_imps)):
                    if i in selected:
                        continue
                    count = sum(Constants.ONE for j in uncovered if remaining_table[i][j])
                    if count > best_count:
                        best_count = count
                        best_imp = i

                if best_imp == -Constants.ONE:
                    break

                selected.append(best_imp)
                for j in range(len(remaining_indices)):
                    if remaining_table[best_imp][j]:
                        uncovered.discard(j)

            all_selected = list(essential) + [remaining_imps[i] for i in selected]
        else:
            all_selected = list(essential)

        expressions = [self._term_to_expression(self.prime_implicants[i]) for i in all_selected]

        if not expressions:
            return Constants.DEFAULT_OUTPUT_ZERO if self.is_sdnf else Constants.DEFAULT_OUTPUT_ONE

        if self.is_sdnf:
            formatted = []
            for term in expressions:
                term = term.strip()
                if term.startswith(Constants.PAREN_OPEN) and term.endswith(Constants.PAREN_CLOSE):
                    term = term[Constants.FIRST_INDEX:-Constants.FIRST_INDEX]
                if f' {Constants.OP_AND_SYMBOL} ' in term:
                    formatted.append(f"{Constants.PAREN_OPEN}{term}{Constants.PAREN_CLOSE}")
                else:
                    formatted.append(term)
            return f" {Constants.OP_OR_SYMBOL} ".join(formatted)
        else:
            formatted = []
            for term in expressions:
                term = term.strip()
                if term.startswith(Constants.PAREN_OPEN) and term.endswith(Constants.PAREN_CLOSE):
                    term = term[Constants.FIRST_INDEX:-Constants.FIRST_INDEX]
                formatted.append(f"{Constants.PAREN_OPEN}{term}{Constants.PAREN_CLOSE}")
            return f" {Constants.OP_AND_SYMBOL} ".join(formatted)

    def print_result(self):
        """Вывод результата минимизации и таблицы покрытий"""
        if not self.indices:
            print(f"\nРезультат минимизации ({'СДНФ' if self.is_sdnf else 'СКНФ'}): {self.result}")
            return

        if len(self.indices) == Constants.POWER_BASE ** self.n:
            print(f"\nРезультат минимизации ({'СДНФ' if self.is_sdnf else 'СКНФ'}): {self.result}")
            return

        formatted_result = self._format_result_with_parentheses(self.result, self.is_sdnf)

        print(f"\nРезультат минимизации ({'СДНФ' if self.is_sdnf else 'СКНФ'}): {formatted_result}")

        if self.prime_implicants and self.indices:
            print("\n" + "=" * Constants.TABLE_WIDTH)
            print("ТАБЛИЦА ПОКРЫТИЙ")
            print("=" * Constants.TABLE_WIDTH)

            max_imp_len = Constants.ZERO
            imp_expressions = []
            for imp in self.prime_implicants:
                expr = self._term_to_expression(imp)
                imp_expressions.append(expr)
                max_imp_len = max(max_imp_len, len(expr))

            imp_width = max(max_imp_len, Constants.MIN_IMP_COL_WIDTH)

            header = "Импликанта" + " " * (imp_width - len("Импликанта"))
            for idx in self.indices:
                binary = self._to_binary(idx)
                header += f" | {binary}  "
            print(header)
            print("-" * (imp_width + Constants.TABLE_COLUMN_SPACING * len(self.indices)))

            for i, (imp, expr) in enumerate(zip(self.prime_implicants, imp_expressions)):
                row = expr + " " * (imp_width - len(expr))
                for j, idx in enumerate(self.indices):
                    covers = self._covers(imp, idx)
                    row += f" |  {Constants.TABLE_COVER_MARK if covers else ' '}   "
                print(row)
            print("=" * 80)

    def _format_result_with_parentheses(self, result: str, is_sdnf: bool) -> str:
        """Форматирование результата с правильными скобками"""
        if not result:
            return result

        if is_sdnf:
            if f' {Constants.OP_OR_SYMBOL} ' in result:
                terms = result.split(f' {Constants.OP_OR_SYMBOL} ')
                formatted_terms = []
                for term in terms:
                    term = term.strip()
                    if term.startswith(Constants.PAREN_OPEN) and term.endswith(Constants.PAREN_CLOSE):
                        term = term[Constants.FIRST_INDEX:-Constants.FIRST_INDEX]
                    if f' {Constants.OP_AND_SYMBOL} ' in term:
                        formatted_terms.append(f"{Constants.PAREN_OPEN}{term}{Constants.PAREN_CLOSE}")
                    else:
                        formatted_terms.append(term)
                return f' {Constants.OP_OR_SYMBOL} '.join(formatted_terms)
            else:
                term = result.strip()
                if term.startswith(Constants.PAREN_OPEN) and term.endswith(Constants.PAREN_CLOSE):
                    term = term[Constants.FIRST_INDEX:-Constants.FIRST_INDEX]
                if f' {Constants.OP_AND_SYMBOL} ' in term:
                    return f"{Constants.PAREN_OPEN}{term}{Constants.PAREN_CLOSE}"
                return term
        else:
            if f' {Constants.OP_AND_SYMBOL} ' in result:
                terms = result.split(f' {Constants.OP_AND_SYMBOL} ')
                formatted_terms = []
                for term in terms:
                    term = term.strip()
                    if term.startswith(Constants.PAREN_OPEN) and term.endswith(Constants.PAREN_CLOSE):
                        term = term[Constants.FIRST_INDEX:-Constants.FIRST_INDEX]
                    formatted_terms.append(f"{Constants.PAREN_OPEN}{term}{Constants.PAREN_CLOSE}")
                return f' {Constants.OP_AND_SYMBOL} '.join(formatted_terms)
            else:
                term = result.strip()
                if term.startswith(Constants.PAREN_OPEN) and term.endswith(Constants.PAREN_CLOSE):
                    term = term[Constants.FIRST_INDEX:-Constants.FIRST_INDEX]
                if f' {Constants.OP_OR_SYMBOL} ' in term:
                    return f"{Constants.PAREN_OPEN}{term}{Constants.PAREN_CLOSE}"
                return term
