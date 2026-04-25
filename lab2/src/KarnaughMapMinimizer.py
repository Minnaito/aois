from src.constants import Constants


class KarnaughMapMinimizer:
    """Класс для минимизации логических функций с помощью карт Карно"""

    def __init__(self, truth_table, variables):
        self.truth_table = truth_table
        self.variables = variables
        self.n = len(variables)
        self.size = Constants.POWER_BASE ** self.n
        self.map = self._build_kmap()

    @staticmethod
    def _get_output(item):
        if isinstance(item, dict):
            return int(item.get(Constants.OUTPUT_KEY, Constants.ZERO))
        return int(item)

    def _get_dimensions(self):
        if self.n == Constants.ONE:
            return Constants.TWO, Constants.ONE, Constants.ONE
        elif self.n == Constants.TWO:
            return Constants.TWO, Constants.TWO, Constants.ONE
        elif self.n == Constants.THREE:
            return Constants.TWO, Constants.FOUR, Constants.ONE
        elif self.n == Constants.FOUR:
            return Constants.FOUR, Constants.FOUR, Constants.ONE
        else:  # 5 переменных
            return Constants.FOUR, Constants.FOUR, Constants.TWO

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
        rows, cols, layers = self._get_dimensions()
        if self.n == Constants.ONE:
            return [cell[Constants.ZERO_INDEX]]
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
            return [(ab >> Constants.ONE) & Constants.ONE, ab & Constants.ONE,
                    (cd >> Constants.ONE) & Constants.ONE, cd & Constants.ONE]
        else:  # n == 5
            layer, row, col = cell
            ab = self._gray_to_bin(row, Constants.TWO)
            cd = self._gray_to_bin(col, Constants.TWO)
            return [(ab >> Constants.ONE) & Constants.ONE, ab & Constants.ONE,
                    (cd >> Constants.ONE) & Constants.ONE, cd & Constants.ONE, layer]

    def _get_cell_value(self, cell):
        """Возвращает значение клетки по координатам с учётом размерности."""
        rows, cols, layers = self._get_dimensions()
        if layers == Constants.ONE:
            return self.map[cell[0]][cell[1]] if len(cell) == 2 else self.map[cell[0]]
        else:
            layer, row, col = cell
            return self.map[layer][row][col]

    def _build_kmap(self):
        if self.n == Constants.ONE:
            return self._build_kmap_1()
        elif self.n == Constants.TWO:
            return self._build_kmap_2()
        elif self.n == Constants.THREE:
            return self._build_kmap_3()
        elif self.n == Constants.FOUR:
            return self._build_kmap_4()
        elif self.n == Constants.FIVE:
            return self._build_kmap_5()
        else:
            raise ValueError("Поддерживается до 5 переменных")

    def _build_kmap_1(self):
        return [self._get_output(self.truth_table[i]) for i in range(Constants.POWER_BASE)]

    def _build_kmap_2(self):
        kmap = [[Constants.ZERO, Constants.ZERO], [Constants.ZERO, Constants.ZERO]]
        for i in range(Constants.FOUR):
            row = (i >> Constants.ONE) & Constants.ONE
            col = i & Constants.ONE
            kmap[row][col] = self._get_output(self.truth_table[i])
        return kmap

    def _build_kmap_3(self):
        kmap = [[Constants.ZERO] * Constants.FOUR for _ in range(Constants.TWO)]
        for i in range(Constants.POWER_BASE ** Constants.THREE):
            row = (i >> Constants.TWO) & Constants.ONE
            bc = i & Constants.THREE
            col = bc ^ (bc >> Constants.ONE)
            kmap[row][col] = self._get_output(self.truth_table[i])
        return kmap

    def _build_kmap_4(self):
        kmap = [[Constants.ZERO] * Constants.FOUR for _ in range(Constants.FOUR)]
        for i in range(Constants.POWER_BASE ** Constants.FOUR):
            ab = (i >> Constants.TWO) & Constants.THREE
            cd = i & Constants.THREE
            row = ab ^ (ab >> Constants.ONE)
            col = cd ^ (cd >> Constants.ONE)
            kmap[row][col] = self._get_output(self.truth_table[i])
        return kmap

    def _build_kmap_5(self):
        kmap = [[[Constants.ZERO] * Constants.FOUR for _ in range(Constants.FOUR)] for _ in range(Constants.TWO)]
        mask = Constants.POWER_BASE ** Constants.FOUR - Constants.ONE
        for i in range(Constants.POWER_BASE ** Constants.FIVE):
            e = i & Constants.ONE
            abcd = (i >> Constants.ONE) & mask
            ab = (abcd >> Constants.TWO) & Constants.THREE
            cd = abcd & Constants.THREE
            row = ab ^ (ab >> Constants.ONE)
            col = cd ^ (cd >> Constants.ONE)
            kmap[e][row][col] = self._get_output(self.truth_table[i])
        return kmap

    def _find_prime_implicants(self):
        if self.map is None:
            return []
        if self.n == Constants.ONE:
            return self._prime_implicants_1()
        return self._prime_implicants_n()

    def _prime_implicants_1(self):
        rows, _, _ = self._get_dimensions()
        prime_implicants = []
        for i in range(rows):
            if self.map[i] == Constants.ONE:
                cells = {(i,)}
                term = self._cells_to_term(cells)
                if not self._has_contradiction(term):
                    prime_implicants.append({'cells': cells, 'term': term})
        prime_implicants.sort(key=lambda x: len(x['cells']), reverse=True)
        return prime_implicants

    def _prime_implicants_n(self):
        rows, cols, layers = self._get_dimensions()
        prime_implicants = []
        possible_heights = [h for h in [1, 2, 4] if h <= rows]
        possible_widths = [w for w in [1, 2, 4] if w <= cols]
        for height in possible_heights:
            for width in possible_widths:
                self._scan_rectangles(height, width, layers, rows, cols, prime_implicants)
        prime_implicants.sort(key=lambda x: len(x['cells']), reverse=True)
        return prime_implicants

    def _scan_rectangles(self, height, width, layers, rows, cols, prime_implicants):
        for layer in range(layers):
            for r in range(rows):
                for c in range(cols):
                    cells, all_ones = self._check_rect(layer, r, c, height, width, layers, rows, cols)
                    if all_ones and cells:
                        self._add_if_maximal(cells, prime_implicants)

    def _check_rect(self, layer, r, c, height, width, layers, rows, cols):
        cells = []
        for i in range(height):
            row_idx = (r + i) % rows
            for j in range(width):
                col_idx = (c + j) % cols
                val = self._rect_value(layer, row_idx, col_idx, layers)
                if val != Constants.ONE:
                    return [], False
                cell = (row_idx, col_idx) if layers == Constants.ONE else (layer, row_idx, col_idx)
                cells.append(cell)
        return cells, True

    def _rect_value(self, layer, row_idx, col_idx, layers):
        if layers == Constants.ONE:
            return self.map[row_idx][col_idx]
        return self.map[layer][row_idx][col_idx]

    def _add_if_maximal(self, cells, prime_implicants):
        cells_set = set(cells)
        term = self._cells_to_term(cells_set)
        if self._has_contradiction(term):
            return
        if not any(cells_set.issubset(imp['cells']) for imp in prime_implicants):
            prime_implicants[:] = [imp for imp in prime_implicants if not imp['cells'].issubset(cells_set)]
            prime_implicants.append({'cells': cells_set, 'term': term})

    def _minimize_dnf(self, prime_implicants):
        if self.map is None:
            return "Ошибка"
        ones = self._collect_ones()
        if not ones:
            return Constants.DEFAULT_OUTPUT_ZERO
        if len(ones) == self._total_cells():
            return Constants.DEFAULT_OUTPUT_ONE
        selected_terms = self._essential_and_greedy(prime_implicants, ones)
        terms = [imp['term'] for imp in selected_terms]
        terms = [t for t in terms if t != Constants.DEFAULT_OUTPUT_ONE]
        if not terms:
            return Constants.DEFAULT_OUTPUT_ONE
        simplified = self._simplify_dnf_terms(terms)
        if len(simplified) == Constants.ONE:
            return simplified[0]
        return " ∨ ".join(simplified)

    def _collect_ones(self):
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
                        if self._rect_value(layer, r, c, layers) == Constants.ONE:
                            ones.append((r, c) if layers == Constants.ONE else (layer, r, c))
        return ones

    def _total_cells(self):
        rows, cols, layers = self._get_dimensions()
        return rows * cols * layers

    def _essential_and_greedy(self, prime_implicants, must_cover):
        uncovered = set(must_cover)
        selected = []
        for cell in must_cover:
            covering = [imp for imp in prime_implicants if cell in imp['cells']]
            if len(covering) == 1:
                imp = covering[0]
                if imp not in selected:
                    selected.append(imp)
                    uncovered -= imp['cells']
        while uncovered:
            best = max(
                (imp for imp in prime_implicants if imp not in selected),
                key=lambda imp: len(imp['cells'] & uncovered),
                default=None
            )
            if best is None or len(best['cells'] & uncovered) == 0:
                break
            selected.append(best)
            uncovered -= best['cells']
        return selected

    def _simplify_dnf_terms(self, terms):
        if not terms:
            return terms
        parsed = [self._parse_term(term) for term in terms]
        changed = True
        while changed:
            changed = False
            parsed = self._absorption(parsed)
            if parsed is False:
                continue
            parsed, changed = self._combine_terms(parsed)
        result = []
        for term, lits in parsed:
            if self._has_contradiction(term) and term not in result:
                continue
            if term not in result:
                result.append(term)
        return result

    def _parse_term(self, term):
        literals = set()
        i = 0
        while i < len(term):
            if term[i] == Constants.OP_NOT:
                literals.add(term[i:i + 2])
                i += 2
            else:
                literals.add(term[i])
                i += 1
        return term, literals

    def _absorption(self, parsed):
        new_parsed = parsed[:]
        for i in range(len(new_parsed)):
            for j in range(len(new_parsed)):
                if i != j and new_parsed[i][1].issubset(new_parsed[j][1]):
                    del new_parsed[j]
                    return new_parsed  
        return parsed

    def _try_combine_pair(self, new_parsed, lits_a, lits_b):
        """Если один из наборов — одиночный литерал, а другой содержит его отрицание,
        порождает упрощённый набор (если его ещё нет). Возвращает True при добавлении."""
        changed = False
        for single_lits, other_lits in ((lits_a, lits_b), (lits_b, lits_a)):
            if len(single_lits) == 1:
                lit = list(single_lits)[0]
                opp = lit[1:] if lit.startswith(Constants.OP_NOT) else Constants.OP_NOT + lit
                if opp in other_lits:
                    new_lits = other_lits - {opp}
                    if new_lits:
                        new_term = self._lits_to_str(new_lits)
                        if not any(new_lits == p[1] for p in new_parsed):
                            new_parsed.append((new_term, new_lits))
                            changed = True
            if changed:
                return True 
        return False

    def _combine_terms(self, parsed):
        new_parsed = parsed[:]
        changed = False
        for i in range(len(new_parsed)):
            for j in range(i + 1, len(new_parsed)):
                if self._try_combine_pair(new_parsed, new_parsed[i][1], new_parsed[j][1]):
                    changed = True
        return new_parsed, changed

    def _lits_to_str(self, literals):
        return ''.join(sorted(literals, key=lambda x: (x.startswith(Constants.OP_NOT), x[-1])))

    def _cells_to_term(self, cells):
        if not cells:
            return Constants.DEFAULT_OUTPUT_ZERO
        if self.n == Constants.ONE:
            vectors = [[cell[0]] for cell in cells]
        else:
            vectors = [self._cell_to_input_vector(cell) for cell in cells]
        term_parts = []
        for var_idx, var_name in enumerate(self.variables):
            values = {vec[var_idx] for vec in vectors}
            if len(values) == 1:
                val = values.pop()
                term_parts.append(var_name if val == Constants.ONE else f"{Constants.OP_NOT}{var_name}")
        if not term_parts:
            return Constants.DEFAULT_OUTPUT_ONE
        if len(term_parts) == 1:
            return term_parts[0]
        return "".join(term_parts)

    def _has_contradiction(self, term: str) -> bool:
        """Проверяет, содержит ли терм x и ¬x одновременно."""
        pos = set()
        neg = set()
        i = 0
        while i < len(term):
            if term[i] == Constants.OP_NOT:
                neg.add(term[i + 1])
                i += 2
            else:
                pos.add(term[i])
                i += 1
        return bool(pos & neg)

    def _minimize_cnf(self):
        if self.map is None:
            return "Ошибка"
        zeros = self._collect_zeros()
        if not zeros:
            return Constants.DEFAULT_OUTPUT_ONE
        if len(zeros) == self._total_cells():
            return Constants.DEFAULT_OUTPUT_ZERO

        temp_map = self._invert_map()
        original_map = self.map
        self.map = temp_map
        prime_implicants = self._find_prime_implicants()
        self.map = original_map

        if not prime_implicants:
            return Constants.DEFAULT_OUTPUT_ONE
        selected_terms = self._essential_and_greedy(prime_implicants, zeros)
        cnf_terms = self._terms_to_cnf(selected_terms)
        if len(cnf_terms) == 1:
            return cnf_terms[0]
        return " ∧ ".join(cnf_terms)

    def _collect_zeros(self):
        rows, cols, layers = self._get_dimensions()
        zeros = []
        if self.n == Constants.ONE:
            for i in range(rows):
                if self.map[i] == Constants.ZERO:
                    zeros.append((i,))
        else:
            for layer in range(layers):
                for r in range(rows):
                    for c in range(cols):
                        if self._rect_value(layer, r, c, layers) == Constants.ZERO:
                            zeros.append((r, c) if layers == Constants.ONE else (layer, r, c))
        return zeros

    def _invert_map(self):
        if self.n == Constants.ONE:
            return [1 - val for val in self.map]
        rows, cols, layers = self._get_dimensions()
        if layers == 1:
            return [[1 - self.map[r][c] for c in range(cols)] for r in range(rows)]
        return [[[1 - self.map[l][r][c] for c in range(cols)] for r in range(rows)] for l in range(layers)]

    def _terms_to_cnf(self, selected_terms):
        cnf_terms = []
        for imp in selected_terms:
            term = imp['term']
            if term == Constants.DEFAULT_OUTPUT_ONE:
                continue
            if term == Constants.DEFAULT_OUTPUT_ZERO:
                cnf_terms.append(Constants.DEFAULT_OUTPUT_ONE)
                continue
            disjuncts = self._disjuncts_from_term(term)
            if len(disjuncts) == 1:
                cnf_terms.append(disjuncts[0])
            else:
                cnf_terms.append(f"({f' ∨ '.join(disjuncts)})")
        return cnf_terms

    def _disjuncts_from_term(self, term_str):
        disjuncts = []
        i = 0
        while i < len(term_str):
            if term_str[i] == Constants.OP_NOT:
                disjuncts.append(term_str[i + 1]) 
                i += 2
            else:
                disjuncts.append(f"{Constants.OP_NOT}{term_str[i]}")  
                i += 1
        return disjuncts

    def print_kmap(self):
        if self.map is None:
            print("\nОшибка: Карта Карно не может быть построена")
            return
        print("\nКарта Карно:")
        if self.n == Constants.ONE:
            self._print_kmap_1()
        elif self.n == Constants.TWO:
            self._print_kmap_2()
        elif self.n == Constants.THREE:
            self._print_kmap_3()
        elif self.n == Constants.FOUR:
            self._print_kmap_4()
        elif self.n == Constants.FIVE:
            self._print_kmap_5()

        prime_implicants = self._find_prime_implicants()
        print(f"\nМинимизированная ДНФ:\n{self._minimize_dnf(prime_implicants)}")
        print(f"\nМинимизированная КНФ:\n{self._minimize_cnf()}")

    def _print_kmap_1(self):
        print("│ a │ f │")
        print(f"│ 0 │ {self.map[0]} │")
        print(f"│ 1 │ {self.map[1]} │")

    def _print_kmap_2(self):
        print("│a\\b│ 0 │ 1 │")
        for i in range(2):
            print(f"│ {i} │ {self.map[i][0]} │ {self.map[i][1]} │")

    def _print_kmap_3(self):
        print("│a\\bc│ 00 │ 01 │ 11 │ 10 │")
        for i in range(2):
            print(f"│ {i}  │  {self.map[i][0]}  │  {self.map[i][1]}  │  {self.map[i][2]}  │  {self.map[i][3]}  │")

    def _print_kmap_4(self):
        print("│AB\\CD│ 00 │ 01 │ 11 │ 10 │")
        ab_labels = ["00", "01", "11", "10"]
        for i in range(4):
            print(f"│ {ab_labels[i]} │  {self.map[i][0]}  │  {self.map[i][1]}  │  {self.map[i][2]}  │  {self.map[i][3]}  │")

    def _print_kmap_5(self):
        gray_3bit = ["000", "001", "011", "010", "110", "111", "101", "100"]
        row_labels = ["00", "01", "11", "10"]
        print("\nКарта Карно для 5 переменных:")
        print("ab \\ cde\t" + "\t".join(gray_3bit))
        print("-" * (15 + 8 * len(gray_3bit)))
        for ab_idx, ab_label in enumerate(row_labels):
            row_str = f"{ab_label}\t\t"
            for cde_label in gray_3bit:
                e = int(cde_label[2])
                cd_bits = cde_label[:2]
                cd_idx = row_labels.index(cd_bits)
                val = self.map[e][ab_idx][cd_idx]
                row_str += f"\t{val}"
            print(row_str)

    def _format_result(self, expr: str) -> str:
        """Форматирование результата с правильными скобками и пробелами"""
        if not expr:
            return expr
        if f' {Constants.OP_OR_SYMBOL} ' in expr:
            terms = expr.split(f' {Constants.OP_OR_SYMBOL} ')
            formatted = []
            for term in terms:
                term = term.strip()
                formatted.append(term)
            return f" {Constants.OP_OR_SYMBOL} ".join(formatted)
        if f' {Constants.OP_AND_SYMBOL} ' in expr:
            return expr
        return expr
