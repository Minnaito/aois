class BooleanFunction:
    def __init__(self, truth_table, input_names):
        self.n = len(input_names)
        self.input_names = input_names
        self.truth_table = truth_table
        assert len(truth_table) == 2 ** self.n, "Длина таблицы истинности не соответствует числу переменных"

    def get_minterms(self):
        """Возвращает индексы наборов, на которых функция равна 1."""
        return [i for i, val in enumerate(self.truth_table) if val == 1]

    def get_maxterms(self):
        """Возвращает индексы наборов, на которых функция равна 0."""
        return [i for i, val in enumerate(self.truth_table) if val == 0]

    def to_sknf(self):
        """Возвращает строку – совершенную конъюнктивную нормальную форму (СКНФ)."""
        maxterms = self.get_maxterms()
        if not maxterms:
            return "1"
        terms = []
        for idx in maxterms:
            bits = [(idx >> (self.n - 1 - k)) & 1 for k in range(self.n)]
            literals = []
            for i, bit in enumerate(bits):
                var = self.input_names[i]
                literals.append(var if bit == 0 else f"~{var}")
            terms.append("(" + " + ".join(literals) + ")")
        return " * ".join(terms)

    def to_sdnf(self):
        """Возвращает строку – совершенную дизъюнктивную нормальную форму (СДНФ)."""
        minterms = self.get_minterms()
        if not minterms:
            return "0"
        terms = []
        for idx in minterms:
            bits = [(idx >> (self.n - 1 - k)) & 1 for k in range(self.n)]
            literals = []
            for i, bit in enumerate(bits):
                var = self.input_names[i]
                literals.append(var if bit == 1 else f"~{var}")
            terms.append("(" + " * ".join(literals) + ")")
        return " + ".join(terms)