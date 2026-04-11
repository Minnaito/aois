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

        if self.n == Constants.ONE:
            prime_implicants = []
            var = self.variables[0]
            if self.map[0] == Constants.ONE and self.map[1] == Constants.ONE:
                return [{'cells': {(0,), (1,)}, 'term': Constants.DEFAULT_OUTPUT_ONE}]
            if self.map[0] == Constants.ONE:
                prime_implicants.append({'cells': {(0,)}, 'term': f'{Constants.OP_NOT}{var}'})
            if self.map[1] == Constants.ONE:
                prime_implicants.append({'cells': {(1,)}, 'term': var})
            return prime_implicants

        rows, cols, layers = self._get_dimensions()
        prime_implicants = []

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
                                if not any(cells_set.issubset(impl['cells']) for impl in prime_implicants):
                                    prime_implicants = [impl for impl in prime_implicants
                                                        if not impl['cells'].issubset(cells_set)]
                                    prime_implicants.append({
                                        'cells': cells_set,
                                        'term': self._cells_to_term(cells_set)
                                    })

        prime_implicants.sort(key=lambda x: len(x['cells']), reverse=True)
        return prime_implicants

    def _cells_to_term(self, cells):
        """
        Преобразование множества клеток в логический терм (конъюнкцию литералов).
        Если переменная не меняется на всех клетках, она входит в терм (с отрицанием или без).
        """
        if not cells:
            return Constants.DEFAULT_OUTPUT_ZERO

        vectors = [self._cell_to_input_vector(cell) for cell in cells]

        term_parts = []
        for var_idx, var_name in enumerate(self.variables):
            values = {vec[var_idx] for vec in vectors}
            if len(values) == Constants.ONE:
                val = values.pop()
                term_parts.append(var_name if val == Constants.ONE else f"{Constants.OP_NOT}{var_name}")

        if not term_parts:
            return Constants.DEFAULT_OUTPUT_ONE
        elif len(term_parts) == Constants.ONE:
            return term_parts[Constants.ZERO_INDEX]
        else:
            return f" {Constants.OP_AND_SYMBOL} ".join(term_parts)

    def _minimize_dnf(self, prime_implicants):
        """Жадное покрытие единиц карты простыми импликантами"""
        if self.map is None:
            return "Ошибка"

        if self.n == Constants.ONE:
            var = self.variables[0]
            if self.map == [0, 0]:
                return Constants.DEFAULT_OUTPUT_ZERO
            if self.map == [1, 1]:
                return Constants.DEFAULT_OUTPUT_ONE
            if self.map == [0, 1]:
                return var
            if self.map == [1, 0]:
                return f"{Constants.OP_NOT}{var}"

        rows, cols, layers = self._get_dimensions()

        ones = []
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

        while uncovered:
            best_impl = None
            best_covered = set()
            for impl in prime_implicants:
                covered = impl['cells'] & uncovered
                if len(covered) > len(best_covered):
                    best_covered = covered
                    best_impl = impl
            if best_impl is None:
                break
            selected_terms.append(best_impl['term'])
            uncovered -= best_covered

        selected_terms = [t for t in selected_terms if t != Constants.DEFAULT_OUTPUT_ONE]
        if not selected_terms:
            return Constants.DEFAULT_OUTPUT_ONE

        simplified = self._simplify_dnf(selected_terms)

        if len(simplified) == Constants.ONE:
            term = simplified[Constants.ZERO_INDEX]
            return f"({term})" if f' {Constants.OP_AND_SYMBOL} ' in term else term

        formatted = []
        for term in simplified:
            formatted.append(f"({term})" if f' {Constants.OP_AND_SYMBOL} ' in term else term)
        return f" {Constants.OP_OR_SYMBOL} ".join(formatted)

    def _simplify_dnf(self, terms):
        """
        Упрощение ДНФ путём удаления поглощаемых термов.
        Например, a ∨ (a ∧ b) = a.
        """
        if not terms:
            return terms

        term_sets = []
        for term in terms:
            if term == Constants.DEFAULT_OUTPUT_ONE:
                return [Constants.DEFAULT_OUTPUT_ONE]
            if term == Constants.DEFAULT_OUTPUT_ZERO:
                continue
            if f' {Constants.OP_AND_SYMBOL} ' in term:
                literals = set(term.split(f' {Constants.OP_AND_SYMBOL} '))
            else:
                literals = {term}
            term_sets.append(literals)

        to_keep = [True] * len(term_sets)
        for i in range(len(term_sets)):
            for j in range(len(term_sets)):
                if i != j and term_sets[i].issuperset(term_sets[j]):
                    to_keep[i] = False
                    break

        result_sets = [term_sets[i] for i in range(len(term_sets)) if to_keep[i]]

        result = []
        for ts in result_sets:
            if not ts:
                continue
            literals = sorted(ts)
            if len(literals) == Constants.ONE:
                result.append(literals[Constants.ZERO_INDEX])
            else:
                result.append(f" {Constants.OP_AND_SYMBOL} ".join(literals))
        return result

    def _minimize_cnf(self):
        """Минимизация КНФ путём инверсии карты и использования алгоритма ДНФ"""
        if self.map is None:
            return "Ошибка"

        if self.n == Constants.ONE:
            var = self.variables[0]
            if self.map == [0, 0]:
                return Constants.DEFAULT_OUTPUT_ZERO
            if self.map == [1, 1]:
                return Constants.DEFAULT_OUTPUT_ONE
            if self.map == [0, 1]:
                return var
            if self.map == [1, 0]:
                return f"{Constants.OP_NOT}{var}"

        rows, cols, layers = self._get_dimensions()

        zeros = []
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

        if layers == Constants.ONE:
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

        while uncovered:
            best_impl = None
            best_covered = set()
            for impl in prime_implicants:
                covered = impl['cells'] & uncovered
                if len(covered) > len(best_covered):
                    best_covered = covered
                    best_impl = impl
            if best_impl is None:
                break

            term = best_impl['term']
            if term == Constants.DEFAULT_OUTPUT_ONE:
                inverted = Constants.DEFAULT_OUTPUT_ZERO
            elif term == Constants.DEFAULT_OUTPUT_ZERO:
                inverted = Constants.DEFAULT_OUTPUT_ONE
            else:
                if f' {Constants.OP_AND_SYMBOL} ' in term:
                    conjuncts = term.split(f' {Constants.OP_AND_SYMBOL} ')
                else:
                    conjuncts = [term]

                disjuncts = []
                for lit in conjuncts:
                    lit = lit.strip()
                    if lit.startswith(Constants.OP_NOT):
                        disjuncts.append(lit[Constants.FIRST_INDEX:])
                    else:
                        disjuncts.append(f"{Constants.OP_NOT}{lit}")
                inverted = f" {Constants.OP_OR_SYMBOL} ".join(disjuncts)

            selected_terms.append(inverted)
            uncovered -= best_covered

        selected_terms = [t for t in selected_terms if t != Constants.DEFAULT_OUTPUT_ONE]
        if not selected_terms:
            return Constants.DEFAULT_OUTPUT_ONE

        if len(selected_terms) == Constants.ONE:
            term = selected_terms[Constants.ZERO_INDEX]
            return f"({term})" if f' {Constants.OP_OR_SYMBOL} ' in term else term
        return f" {Constants.OP_AND_SYMBOL} ".join([f"({term})" for term in selected_terms])

    def print_kmap(self):
        """Печать карты Карно и результатов минимизации"""
        if self.map is None:
            print("\nОшибка: Карта Карно не может быть построена")
            return

        print("\nКарта Карно:")

        if self.n == Constants.ONE:
            print("│ a │ f │")
            print(f"│ {Constants.ZERO} │ {self.map[Constants.ZERO_INDEX]} │")
            print(f"│ {Constants.ONE} │ {self.map[Constants.FIRST_INDEX]} │")
        elif self.n == Constants.TWO:
            print("│a\\b│ 0 │ 1 │")
            for i in range(Constants.TWO):
                print(f"│ {i} │ {self.map[i][Constants.ZERO_INDEX]} │ {self.map[i][Constants.FIRST_INDEX]} │")
        elif self.n == Constants.THREE:
            print("│a\\bc│ 00 │ 01 │ 11 │ 10 │")
            for i in range(Constants.TWO):
                print(f"│ {i}  │  {self.map[i][Constants.ZERO_INDEX]}  │  {self.map[i][Constants.FIRST_INDEX]}  │  {self.map[i][Constants.SECOND_INDEX]}  │  {self.map[i][Constants.THIRD_INDEX]}  │")
        elif self.n == Constants.FOUR:
            print("│AB\\CD│ 00 │ 01 │ 11 │ 10 │")
            ab_labels = ["00", "01", "11", "10"]
            for i in range(Constants.FOUR):
                print(f"│ {ab_labels[i]} │  {self.map[i][Constants.ZERO_INDEX]}  │  {self.map[i][Constants.FIRST_INDEX]}  │  {self.map[i][Constants.SECOND_INDEX]}  │  {self.map[i][Constants.THIRD_INDEX]}  │")
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
