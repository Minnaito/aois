from src.constants import Constants


class KarnaughMapMinimizer:
    """Минимизатор методом карт Карно"""

    def __init__(self, truth_table: list, variables: list):
        self.truth_table = truth_table
        self.variables = variables
        self.n = len(variables)
        self.kmap = {}
        self.minimized_function = ""
        self._build_kmap()
        self._minimize()

    def _build_kmap(self):
        """Построение карты Карно"""
        if self.n == 2:
            self._build_2d_kmap()
        elif self.n == 3:
            self._build_3d_kmap()
        elif self.n == 4:
            self._build_4d_kmap()
        else:
            self._build_5d_kmap()

    def _build_2d_kmap(self):
        """Построение карты для 2 переменных"""
        self.kmap = {}
        order = Constants.get_kmap_order(self.n)

        for row1 in order:
            self.kmap[row1] = 0

        for row in self.truth_table:
            inputs = row['inputs']
            # Исправление: проверяем длину inputs
            if len(inputs) >= 2:
                key = f"{inputs[0]}{inputs[1]}"
                self.kmap[key] = row['output']

    def _build_3d_kmap(self):
        """Построение карты для 3 переменных"""
        self.kmap = {}
        order = Constants.get_kmap_order(self.n)

        for a in [0, 1]:
            for bc in order:
                key = f"{a}{bc}"
                self.kmap[key] = 0

        for row in self.truth_table:
            inputs = row['inputs']
            if len(inputs) >= 3:
                bc = f"{inputs[1]}{inputs[2]}"
                key = f"{inputs[0]}{bc}"
                self.kmap[key] = row['output']

    def _build_4d_kmap(self):
        """Построение карты для 4 переменных"""
        self.kmap = {}
        order = Constants.get_kmap_order(self.n)

        for ab in order:
            for cd in order:
                key = f"{ab}{cd}"
                self.kmap[key] = 0

        for row in self.truth_table:
            inputs = row['inputs']
            if len(inputs) >= 4:
                ab = f"{inputs[0]}{inputs[1]}"
                cd = f"{inputs[2]}{inputs[3]}"
                key = f"{ab}{cd}"
                self.kmap[key] = row['output']

    def _build_5d_kmap(self):
        """Построение карты для 5 переменных"""
        self.kmap = {}
        order = Constants.get_kmap_order(self.n)

        for e in [0, 1]:
            for ab in order:
                for cd in order:
                    key = f"{e}{ab}{cd}"
                    self.kmap[key] = 0

        for row in self.truth_table:
            inputs = row['inputs']
            if len(inputs) >= 5:
                e = inputs[0]
                ab = f"{inputs[1]}{inputs[2]}"
                cd = f"{inputs[3]}{inputs[4]}"
                key = f"{e}{ab}{cd}"
                self.kmap[key] = row['output']

    def _get_neighbors(self, key: str) -> list:
        """Получение соседних клеток по горизонтали и вертикали"""
        neighbors = []
        order = Constants.get_kmap_order(self.n)

        if self.n == 2:
            bits = list(key)
            for i in range(2):
                for delta in [-1, 1]:
                    new_bits = bits.copy()
                    new_bits[i] = str((int(bits[i]) + delta) % Constants.POWER_BASE)
                    neighbors.append(''.join(new_bits))

        elif self.n == 3:
            a = key[0]
            bc = key[1:]
            bc_index = order.index(bc)

            for delta in [-1, 1]:
                new_bc = order[(bc_index + delta) % len(order)]
                neighbors.append(f"{a}{new_bc}")

            new_a = '1' if a == '0' else '0'
            neighbors.append(f"{new_a}{bc}")

        elif self.n == 4:
            ab = key[:2]
            cd = key[2:]
            ab_order = order
            cd_order = order

            ab_index = ab_order.index(ab)
            cd_index = cd_order.index(cd)

            for delta in [-1, 1]:
                new_cd = cd_order[(cd_index + delta) % len(cd_order)]
                neighbors.append(f"{ab}{new_cd}")

            for delta in [-1, 1]:
                new_ab = ab_order[(ab_index + delta) % len(ab_order)]
                neighbors.append(f"{new_ab}{cd}")

        return neighbors

    def _find_rectangles(self) -> list:
        """Поиск максимальных прямоугольных областей из единиц"""
        ones = {key for key, value in self.kmap.items() if value == 1}
        if not ones:
            return []

        implicants = []

        sizes = Constants.get_rect_sizes(self.n)

        if self.n == 3:
            rows = [0, 1]  # a
            cols = Constants.get_kmap_order(self.n)  # bc
        elif self.n == 4:
            rows = Constants.get_kmap_order(self.n)  # ab
            cols = Constants.get_kmap_order(self.n)  # cd
        else:
            rows = [0, 1]
            cols = [0, 1]

        for height, width in sizes:
            for i in range(len(rows)):
                for j in range(len(cols)):
                    rect_cells = []
                    valid = True

                    for di in range(height):
                        for dj in range(width):
                            row_idx = (i + di) % len(rows)
                            col_idx = (j + dj) % len(cols)

                            if self.n == 3:
                                key = f"{rows[row_idx]}{cols[col_idx]}"
                            elif self.n == 4:
                                key = f"{rows[row_idx]}{cols[col_idx]}"
                            else:
                                key = f"{rows[row_idx]}{cols[col_idx]}"

                            if key not in ones:
                                valid = False
                                break
                            rect_cells.append(key)
                        if not valid:
                            break

                    if valid and rect_cells:
                        implicant = self._create_implicant(rect_cells)
                        if implicant not in implicants:
                            implicants.append(implicant)

        max_implicants = []
        for i, imp in enumerate(implicants):
            is_maximal = True
            for j, other_imp in enumerate(implicants):
                if i != j and self._covers_implicant(other_imp, imp):
                    is_maximal = False
                    break
            if is_maximal:
                max_implicants.append(imp)

        return max_implicants

    def _covers_implicant(self, imp1: str, imp2: str) -> bool:
        """Проверяет, покрывает ли импликанта imp1 импликанту imp2"""
        for i in range(len(imp1)):
            if imp1[i] != Constants.BINARY_X and imp1[i] != imp2[i]:
                return False
        return True

    def _create_implicant(self, cells: list) -> str:
        """Создает импликанту из списка клеток"""
        if not cells:
            return ""

        result = [Constants.BINARY_X] * self.n

        for i in range(self.n):
            values = set()
            for cell in cells:
                values.add(cell[i])
            if len(values) == 1:
                result[i] = values.pop()

        return ''.join(result)

    def _key_to_term(self, implicant: str) -> str:
        """Преобразование импликанты в строковое представление"""
        terms = []
        for i, char in enumerate(implicant):
            if char == Constants.BINARY_ONE:
                terms.append(self.variables[i])
            elif char == Constants.BINARY_ZERO:
                terms.append(f"{Constants.OP_NOT}{self.variables[i]}")
        return " ∧ ".join(terms) if terms else Constants.DEFAULT_OUTPUT_ONE

    def _get_all_ones(self) -> list:
        """Получение всех единиц из карты Карно"""
        ones = []
        for key, value in self.kmap.items():
            if value == 1:
                ones.append(key)
        return ones

    def _minimize(self):
        """Минимизация"""
        rectangles = self._find_rectangles()

        if not rectangles:
            ones = self._get_all_ones()
            if ones:
                terms = [self._key_to_term(key) for key in ones]
                self.minimized_function = " ∨ ".join(['(' + t + ')' for t in terms])
            else:
                self.minimized_function = Constants.DEFAULT_OUTPUT_ZERO
            return

        terms = []
        for imp in rectangles:
            term = self._key_to_term(imp)
            if term not in terms:
                terms.append(term)

        essential_implicants = self._find_essential_implicants(rectangles)
        if essential_implicants:
            terms = [self._key_to_term(imp) for imp in essential_implicants]

        self.minimized_function = " ∨ ".join(['(' + t + ')' for t in terms])

    def _find_essential_implicants(self, implicants: list) -> list:
        """Находит существенные импликанты"""
        if not implicants:
            return []

        ones = {key for key, value in self.kmap.items() if value == 1}

        coverage = {}
        for one in ones:
            coverage[one] = []
            for imp in implicants:
                if self._covers_implicant(imp, one):
                    coverage[one].append(imp)

        essential = set()
        for one, covering_imps in coverage.items():
            if len(covering_imps) == 1:
                essential.add(covering_imps[0])

        covered = set()
        for imp in essential:
            for one in ones:
                if self._covers_implicant(imp, one):
                    covered.add(one)

        if len(covered) < len(ones):
            remaining = ones - covered
            for imp in implicants:
                if imp not in essential:
                    essential.add(imp)
                    break

        return list(essential)

    def get_minimized_function(self) -> str:
        """Получение минимизированной функции"""
        return self.minimized_function

    def print_kmap(self):
        """Вывод карты Карно"""
        print("\nКарта Карно:")
        order = Constants.get_kmap_order(self.n)

        if self.n == 2:
            print("\n    00  01  11  10")
            print(f"0   {self.kmap.get('00', 0)}   {self.kmap.get('01', 0)}   {self.kmap.get('11', 0)}   {self.kmap.get('10', 0)}")

        elif self.n == 3:
            print("\n      00  01  11  10")
            for a in [0, 1]:
                row = f"{a}    "
                for bc in order:
                    key = f"{a}{bc}"
                    row += f"{self.kmap.get(key, 0)}   "
                print(row)

        elif self.n == 4:
            print("\n       00   01   11   10")
            for ab in order:
                row = f"{ab}   "
                for cd in order:
                    key = f"{ab}{cd}"
                    row += f"{self.kmap.get(key, 0)}    "
                print(row)

        else:
            print("\nДля 5 переменных:")
            for e in [0, 1]:
                print(f"\ne = {e}:")
                print("       00   01   11   10")
                for ab in order:
                    row = f"{ab}   "
                    for cd in order:
                        key = f"{e}{ab}{cd}"
                        row += f"{self.kmap.get(key, 0)}    "
                print(row)

        print(f"\nРезультат минимизации: {self.minimized_function}")