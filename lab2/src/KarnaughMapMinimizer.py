from src.constants import Constants


class KarnaughMapMinimizer:
    """Класс для минимизации логических функций с помощью карт Карно"""

    def __init__(self, truth_table, variables):
        self.truth_table = truth_table
        self.variables = variables
        self.n = len(variables)
        self.size = Constants.POWER_BASE ** self.n
        self.map = self._build_kmap()

    def _get_output(self, item):
        """Извлечение значения выхода из элемента таблицы истинности"""
        if isinstance(item, dict):
            return int(item.get(Constants.OUTPUT_KEY, Constants.ZERO))
        return int(item)

    def _build_kmap(self):
        """Создание карты Карно соответствующей размерности"""
        if self.n == Constants.ONE:
            return [self._get_output(self.truth_table[i]) for i in range(Constants.POWER_BASE)]
        elif self.n == Constants.TWO:
            kmap = [[Constants.ZERO, Constants.ZERO], [Constants.ZERO, Constants.ZERO]]
            for i in range(Constants.FOUR):
                row = (i >> Constants.ONE) & Constants.ONE
                col = i & Constants.ONE
                kmap[row][col] = self._get_output(self.truth_table[i])
            return kmap
        elif self.n == Constants.THREE:
            kmap = [[Constants.ZERO, Constants.ZERO, Constants.ZERO, Constants.ZERO] for _ in range(Constants.TWO)]
            for i in range(Constants.POWER_BASE ** Constants.THREE):
                row = (i >> Constants.TWO) & Constants.ONE
                bc = i & Constants.THREE
                col = bc ^ (bc >> Constants.ONE)
                kmap[row][col] = self._get_output(self.truth_table[i])
            return kmap
        elif self.n == Constants.FOUR:
            kmap = [[Constants.ZERO, Constants.ZERO, Constants.ZERO, Constants.ZERO] for _ in range(Constants.FOUR)]
            for i in range(Constants.POWER_BASE ** Constants.FOUR):
                ab = (i >> Constants.TWO) & Constants.THREE
                cd = i & Constants.THREE
                row = ab ^ (ab >> Constants.ONE)
                col = cd ^ (cd >> Constants.ONE)
                kmap[row][col] = self._get_output(self.truth_table[i])
            return kmap
        elif self.n == Constants.FIVE:
            kmap = [[[Constants.ZERO, Constants.ZERO, Constants.ZERO, Constants.ZERO] for _ in range(Constants.FOUR)] for _ in range(Constants.TWO)]
            for i in range(Constants.POWER_BASE ** Constants.FIVE):
                e = i & Constants.ONE
                abcd = (i >> Constants.ONE) & Constants.POWER_BASE ** Constants.FOUR - Constants.ONE  # 15
                ab = (abcd >> Constants.TWO) & Constants.THREE
                cd = abcd & Constants.THREE
                row = ab ^ (ab >> Constants.ONE)
                col = cd ^ (cd >> Constants.ONE)
                kmap[e][row][col] = self._get_output(self.truth_table[i])
            return kmap
        else:
            raise ValueError("Поддерживается до 5 переменных")

    def _get_dimensions(self):
        """Возвращает (rows, cols, layers) для текущей карты"""
        if self.n == Constants.ONE:
            return (Constants.TWO, Constants.ONE, Constants.ONE)
        elif self.n == Constants.TWO:
            return (Constants.TWO, Constants.TWO, Constants.ONE)
        elif self.n == Constants.THREE:
            return (Constants.TWO, Constants.FOUR, Constants.ONE)
        elif self.n == Constants.FOUR:
            return (Constants.FOUR, Constants.FOUR, Constants.ONE)
        else:  # n == 5
            return (Constants.FOUR, Constants.FOUR, Constants.TWO)

    @staticmethod
    def _gray_to_bin(gray, bits):
        """Преобразование кода Грея в двоичный код"""
        bin_val = gray
        mask = gray >> Constants.ONE
        while mask:
            bin_val ^= mask
            mask >>= Constants.ONE
        return bin_val

    def _cell_to_input_vector(self, cell):
        """
        Преобразование координат клетки в вектор значений переменных (0/1).
        cell: для n<=4 - (row, col); для n=5 - (layer, row, col)
        """
        rows, cols, layers = self._get_dimensions()
        if self.n == Constants.ONE:
            row = cell[Constants.ZERO_INDEX]
            return [row]
        elif self.n == Constants.TWO:
            row, col = cell
            return [row, col]
        elif self.n == Constants.THREE:
            row, col = cell
            bc = self._gray_to_bin(col, Constants.TWO)
            return [row, (bc >> Constants.ONE) & Constants.ONE, bc & Constants.ONE]
        elif self.n == Constants.FOUR:
            row, col = cell
            ab = self._gray_to_bin(row, Constants.TWO)
            cd = self._gray_to_bin(col, Constants.TWO)
            return [(ab >> Constants.ONE) & Constants.ONE, ab & Constants.ONE, (cd >> Constants.ONE) & Constants.ONE, cd & Constants.ONE]
        else:  # n == 5
            layer, row, col = cell
            ab = self._gray_to_bin(row, Constants.TWO)
            cd = self._gray_to_bin(col, Constants.TWO)
            return [(ab >> Constants.ONE) & Constants.ONE, ab & Constants.ONE, (cd >> Constants.ONE) & Constants.ONE, cd & Constants.ONE, layer]

    def _find_prime_implicants(self):
        """Возвращает список простых импликант (максимальных прямоугольников из единиц)"""
        if self.map is None:
            return []

        rows, cols, layers = self._get_dimensions()
        prime_implicants = []

        if self.n == Constants.ONE:
            for i in range(rows):
                if self.map[i] == Constants.ONE:
                    cells = {(i,)}
                    term = self._cells_to_term(cells)
                    if not self._has_contradiction(term):
                        prime_implicants.append({
                            'cells': cells,
                            'term': term
                        })
            prime_implicants.sort(key=lambda x: len(x['cells']), reverse=True)
            return prime_implicants

        possible_heights = [h for h in [Constants.ONE, Constants.TWO, Constants.FOUR] if h <= rows]
        possible_widths = [w for w in [Constants.ONE, Constants.TWO, Constants.FOUR] if w <= cols]

        for height in possible_heights:
            for width in possible_widths:
                for layer in range(layers):
                    for r in range(rows):
                        for c in range(cols):
                            cells = []
                            all_ones = True
                            for i in range(height):
                                row_idx = (r + i) % rows
                                for j in range(width):
                                    col_idx = (c + j) % cols
                                    if layers == Constants.ONE:
                                        val = self.map[row_idx][col_idx]
                                    else:
                                        val = self.map[layer][row_idx][col_idx]

                                    if val != Constants.ONE:
                                        all_ones = False
                                        break
                                    cell = (row_idx, col_idx) if layers == Constants.ONE else (layer, row_idx, col_idx)
                                    cells.append(cell)
                                if not all_ones:
                                    break
                            if all_ones and cells:
                                cells_set = set(cells)
                                term = self._cells_to_term(cells_set)

                                if self._has_contradiction(term):
                                    continue

                                if not any(cells_set.issubset(impl['cells']) for impl in prime_implicants):
                                    # Удаляем те, которые являются подмножеством новой
                                    prime_implicants = [impl for impl in prime_implicants
                                                        if not impl['cells'].issubset(cells_set)]
                                    prime_implicants.append({
                                        'cells': cells_set,
                                        'term': term
                                    })

        prime_implicants.sort(key=lambda x: len(x['cells']), reverse=True)
        return prime_implicants
    def _has_contradiction(self, term: str) -> bool:
        """Проверяет, содержит ли терм противоречивые литералы (x и ¬x)"""
        vars_positive = set()
        vars_negative = set()

        i = Constants.ZERO
        while i < len(term):
            if i + Constants.ONE < len(term) and term[i] == '¬':
                vars_negative.add(term[i + Constants.ONE])
                i += Constants.TWO
            else:
                vars_positive.add(term[i])
                i += Constants.ONE

        return bool(vars_positive & vars_negative)

    def _minimize_dnf(self, prime_implicants):
        """Жадное покрытие единиц карты простыми импликантами"""
        if self.map is None:
            return "Ошибка"

        rows, cols, layers = self._get_dimensions()

        ones = []

        if self.n == Constants.ONE:
            for i in range(rows):
                if self.map[i] == Constants.ONE:
                    ones.append((i,))
        else:
            for layer in range(layers):
                for r in range(rows):
                    for c in range(cols):
                        if layers == Constants.ONE:
                            if self.map[r][c] == Constants.ONE:
                                ones.append((r, c))
                        else:
                            if self.map[layer][r][c] == Constants.ONE:
                                ones.append((layer, r, c))

        if not ones:
            return Constants.DEFAULT_OUTPUT_ZERO
        total_cells = rows * cols * layers
        if len(ones) == total_cells:
            return Constants.DEFAULT_OUTPUT_ONE

        uncovered = set(ones)
        selected_terms = []
        selected_cells = []

        for cell in ones:
            covering_imps = [imp for imp in prime_implicants if cell in imp['cells']]
            if len(covering_imps) == Constants.ONE:
                imp = covering_imps[Constants.ZERO_INDEX]
                if imp not in selected_terms:
                    selected_terms.append(imp)
                    selected_cells.append(imp)
                    uncovered -= imp['cells']

        while uncovered:
            best_impl = None
            best_covered = set()
            for impl in prime_implicants:
                if impl in selected_cells:
                    continue
                covered = impl['cells'] & uncovered
                if len(covered) > len(best_covered):
                    best_covered = covered
                    best_impl = impl

            if best_impl is None or len(best_covered) == Constants.ZERO:
                break

            selected_terms.append(best_impl)
            selected_cells.append(best_impl)
            uncovered -= best_covered

        terms = [imp['term'] for imp in selected_terms]

        terms = [t for t in terms if t != Constants.DEFAULT_OUTPUT_ONE]
        if not terms:
            return Constants.DEFAULT_OUTPUT_ONE

        simplified = self._simplify_dnf_terms(terms)

        if len(simplified) == Constants.ONE:
            return simplified[Constants.ZERO_INDEX]
        return " ∨ ".join(simplified)

    def _simplify_dnf_terms(self, terms):
        """Упрощение ДНФ путём поглощения и склеивания"""
        if not terms:
            return terms

        parsed = []
        for term in terms:
            literals = set()
            i = Constants.ZERO
            while i < len(term):
                if term[i] == Constants.OP_NOT:
                    literals.add(term[i:i + Constants.TWO]) 
                    i += Constants.TWO
                else:
                    literals.add(term[i]) 
                    i += Constants.ONE
            parsed.append((term, literals))

        changed = True
        while changed:
            changed = False
            to_remove = set()

            for i in range(len(parsed)):
                for j in range(len(parsed)):
                    if i != j and parsed[i][Constants.FIRST_INDEX].issubset(parsed[j][Constants.FIRST_INDEX]):
                        # i-й терм поглощает j-й
                        to_remove.add(j)
                        changed = True

            if to_remove:
                parsed = [parsed[k] for k in range(len(parsed)) if k not in to_remove]
                continue

            for i in range(len(parsed)):
                for j in range(i + Constants.ONE, len(parsed)):
                    term1_lits = parsed[i][Constants.FIRST_INDEX]
                    term2_lits = parsed[j][Constants.FIRST_INDEX]

                    if len(term1_lits) == Constants.ONE:
                        lit = list(term1_lits)[Constants.ZERO_INDEX]
                        opposite = lit[Constants.FIRST_INDEX:] if lit.startswith(
                            Constants.OP_NOT) else f"{Constants.OP_NOT}{lit}"
                        if opposite in term2_lits:
                            # Упрощаем второй терм, убирая отрицание
                            new_lits = term2_lits - {opposite}
                            if new_lits and not any(new_lits == p[Constants.FIRST_INDEX] for p in parsed):
                                new_term = ''.join(sorted(new_lits, key=lambda x: (x.startswith(Constants.OP_NOT),
                                                                                   x[-Constants.FIRST_INDEX])))
                                parsed.append((new_term, new_lits))
                                changed = True

                    if len(term2_lits) == Constants.ONE:
                        lit = list(term2_lits)[Constants.ZERO_INDEX]
                        opposite = lit[Constants.FIRST_INDEX:] if lit.startswith(
                            Constants.OP_NOT) else f"{Constants.OP_NOT}{lit}"
                        if opposite in term1_lits:
                            new_lits = term1_lits - {opposite}
                            if new_lits and not any(new_lits == p[Constants.FIRST_INDEX] for p in parsed):
                                new_term = ''.join(sorted(new_lits, key=lambda x: (x.startswith(Constants.OP_NOT),
                                                                                   x[-Constants.FIRST_INDEX])))
                                parsed.append((new_term, new_lits))
                                changed = True

        result = []
        for term, lits in parsed:
            if self._has_contradiction(term):
                continue
            if term not in result:
                result.append(term)

        return result

    def _cells_to_term(self, cells):
        """
        Преобразование множества клеток в логический терм.
        """
        if not cells:
            return Constants.DEFAULT_OUTPUT_ZERO

        if self.n == Constants.ONE:
            vectors = []
            for cell in cells:
                vectors.append([cell[Constants.ZERO_INDEX]])
        else:
            vectors = [self._cell_to_input_vector(cell) for cell in cells]

        term_parts = []
        for var_idx, var_name in enumerate(self.variables):
            values = {vec[var_idx] for vec in vectors}
            if len(values) == Constants.ONE:
                val = values.pop()
                if val == Constants.ONE:
                    term_parts.append(var_name)
                else:
                    term_parts.append(f"{Constants.OP_NOT}{var_name}")

        if not term_parts:
            return Constants.DEFAULT_OUTPUT_ONE
        elif len(term_parts) == Constants.ONE:
            return term_parts[Constants.ZERO_INDEX]
        else:
            return "".join(term_parts)

    def _has_contradiction(self, term: str) -> bool:
        """Проверяет, содержит ли терм противоречивые литералы (x и !x)"""
        vars_positive = set()
        vars_negative = set()

        i = Constants.ZERO
        while i < len(term):
            if term[i] == Constants.OP_NOT:
                vars_negative.add(term[i + Constants.ONE])
                i += Constants.TWO
            else:
                vars_positive.add(term[i])
                i += Constants.ONE
        return bool(vars_positive & vars_negative)

    def _simplify_term_with_others(self, term, all_terms):
        """Упрощает терм, учитывая другие термы (e ∨ a¬e → e ∨ a)"""

        if len(term) == Constants.ONE:
            return term

        single_vars = {t for t in all_terms if len(t) == Constants.ONE}

        result_parts = []
        i = Constants.ZERO
        while i < len(term):
            if i + Constants.ONE < len(term) and term[i:i + Constants.TWO] == '¬':
                var = term[i + Constants.TWO] if i + Constants.TWO < len(term) else ''
                if var not in single_vars:
                    result_parts.append(term[i:i + Constants.TWO])
                i += Constants.TWO
            else:
                result_parts.append(term[i])
                i += Constants.ONE

        simplified = ''.join(result_parts)
        return simplified if simplified else term

    def _minimize_cnf(self):
        """Минимизация КНФ путём инверсии карты и использования алгоритма ДНФ"""
        if self.map is None:
            return "Ошибка"

        rows, cols, layers = self._get_dimensions()

        # Собираем координаты нулей
        zeros = []

        # Для 1 переменной особый случай
        if self.n == Constants.ONE:
            for i in range(rows):
                if self.map[i] == Constants.ZERO:
                    zeros.append((i,))
        else:
            for layer in range(layers):
                for r in range(rows):
                    for c in range(cols):
                        if layers == Constants.ONE:
                            if self.map[r][c] == Constants.ZERO:
                                zeros.append((r, c))
                        else:
                            if self.map[layer][r][c] == Constants.ZERO:
                                zeros.append((layer, r, c))

        if not zeros:
            return Constants.DEFAULT_OUTPUT_ONE
        total_cells = rows * cols * layers
        if len(zeros) == total_cells:
            return Constants.DEFAULT_OUTPUT_ZERO

        if self.n == Constants.ONE:
            temp_map = [Constants.ONE - self.map[i] for i in range(rows)]
        elif layers == Constants.ONE:
            temp_map = [[Constants.ONE - self.map[r][c] for c in range(cols)] for r in range(rows)]
        else:
            temp_map = [[[Constants.ONE - self.map[l][r][c] for c in range(cols)] for r in range(rows)] for l in
                        range(layers)]

        original_map = self.map
        self.map = temp_map
        prime_implicants = self._find_prime_implicants()
        self.map = original_map

        if not prime_implicants:
            return Constants.DEFAULT_OUTPUT_ONE

        uncovered = set(zeros)
        selected_terms = []
        selected_cells = []

        for cell in zeros:
            covering_imps = [imp for imp in prime_implicants if cell in imp['cells']]
            if len(covering_imps) == Constants.ONE:
                imp = covering_imps[Constants.ZERO_INDEX]
                if imp not in selected_terms:
                    selected_terms.append(imp)
                    selected_cells.append(imp)
                    uncovered -= imp['cells']

        while uncovered:
            best_impl = None
            best_covered = set()
            for impl in prime_implicants:
                if impl in selected_cells:
                    continue
                covered = impl['cells'] & uncovered
                if len(covered) > len(best_covered):
                    best_covered = covered
                    best_impl = impl

            if best_impl is None or len(best_covered) == Constants.ZERO:
                break

            selected_terms.append(best_impl)
            selected_cells.append(best_impl)
            uncovered -= best_covered

        cnf_terms = []
        for imp in selected_terms:
            term = imp['term']
            if term == Constants.DEFAULT_OUTPUT_ONE:
                continue
            elif term == Constants.DEFAULT_OUTPUT_ZERO:
                cnf_terms.append(Constants.DEFAULT_OUTPUT_ONE)
                continue

            disjuncts = []
            i = Constants.ZERO
            while i < len(term):
                if term[i] == Constants.OP_NOT:
                    disjuncts.append(term[i + Constants.ONE])
                    i += Constants.TWO
                else:
                    disjuncts.append(f"{Constants.OP_NOT}{term[i]}")
                    i += Constants.ONE

            if len(disjuncts) == Constants.ONE:
                cnf_term = disjuncts[Constants.ZERO_INDEX]
            else:
                cnf_term = f"({f' {Constants.OP_OR_SYMBOL} '.join(disjuncts)})"
            cnf_terms.append(cnf_term)

        if not cnf_terms:
            return Constants.DEFAULT_OUTPUT_ONE

        if len(cnf_terms) == Constants.ONE:
            return cnf_terms[Constants.ZERO_INDEX]
        return f" {Constants.OP_AND_SYMBOL} ".join(cnf_terms)

    def print_kmap(self):
        """Печать карты Карно и результатов минимизации"""
        if self.map is None:
            print("\nОшибка: Карта Карно не может быть построена")
            return

        print("\nКарта Карно:")

        if self.n == Constants.ONE:
            print("│ a │ f │")
            print(f"│ 0 │ {self.map[Constants.ZERO_INDEX]} │")
            print(f"│ 1 │ {self.map[Constants.FIRST_INDEX]} │")
        elif self.n == Constants.TWO:
            print("│a\\b│ 0 │ 1 │")
            for i in range(Constants.TWO):
                print(f"│ {i} │ {self.map[i][Constants.ZERO_INDEX]} │ {self.map[i][Constants.FIRST_INDEX]} │")
        elif self.n == Constants.THREE:
            print("│a\\bc│ 00 │ 01 │ 11 │ 10 │")
            for i in range(Constants.TWO):
                print(
                    f"│ {i}  │  {self.map[i][Constants.ZERO_INDEX]}  │  {self.map[i][Constants.FIRST_INDEX]}  │  {self.map[i][Constants.SECOND_INDEX]}  │  {self.map[i][Constants.THIRD_INDEX]}  │")
        elif self.n == Constants.FOUR:
            print("│AB\\CD│ 00 │ 01 │ 11 │ 10 │")
            ab_labels = ["00", "01", "11", "10"]
            for i in range(Constants.FOUR):
                print(
                    f"│ {ab_labels[i]} │  {self.map[i][Constants.ZERO_INDEX]}  │  {self.map[i][Constants.FIRST_INDEX]}  │  {self.map[i][Constants.SECOND_INDEX]}  │  {self.map[i][Constants.THIRD_INDEX]}  │")
        elif self.n == Constants.FIVE:
            gray_3bit = ["000", "001", "011", "010", "110", "111", "101", "100"]
            row_labels = ["00", "01", "11", "10"]
            print("\nКарта Карно для 5 переменных:")
            print("ab \\ cde\t" + "\t".join(gray_3bit))
            print("-" * (15 + 8 * len(gray_3bit)))
            for ab_idx, ab_label in enumerate(row_labels):
                row_str = f"{ab_label}\t\t"
                for cde_label in gray_3bit:
                    e = int(cde_label[Constants.TWO])
                    cd_bits = cde_label[:Constants.TWO]
                    cd_idx = row_labels.index(cd_bits)
                    val = self.map[e][ab_idx][cd_idx]
                    row_str += f"\t{val}"
                print(row_str)

        prime_implicants = self._find_prime_implicants()
        minimized_dnf = self._minimize_dnf(prime_implicants)
        print(f"\nМинимизированная ДНФ:\n{minimized_dnf}")

        minimized_cnf = self._minimize_cnf()
        print(f"\nМинимизированная КНФ:\n{minimized_cnf}")

def _format_result(self, expr: str) -> str:
            """Форматирование результата с правильными скобками и пробелами"""
            if not expr:
                return expr

            if f' {Constants.OP_OR_SYMBOL} ' in expr:
                terms = expr.split(f' {Constants.OP_OR_SYMBOL} ')
                formatted = []
                for term in terms:
                    term = term.strip()
                    if len(term) > Constants.ONE and Constants.OP_OR_SYMBOL not in term and Constants.OP_AND_SYMBOL not in term:
                        # Слитный терм типа ab!c
                        if any(c in term for c in Constants.OP_NOT):
                            formatted.append(term)
                        else:
                            formatted.append(term)
                    else:
                        formatted.append(term)
                return f" {Constants.OP_OR_SYMBOL} ".join(formatted)

            if f' {Constants.OP_AND_SYMBOL} ' in expr:
                return expr

            return expr
