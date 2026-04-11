"""Класс для определения принадлежности функции к классам Поста"""

from src.constants import Constants


class PostClassesAnalyzer:
    """Анализатор принадлежности к классам Поста"""

    def __init__(self, truth_table: list, variables: list):
        self.truth_table = truth_table
        self.variables = variables
        self.results = {}
        self._analyze()

    def _analyze(self):
        """Анализ всех классов Поста"""
        self.results[Constants.CLASS_T0] = self._check_t0()
        self.results[Constants.CLASS_T1] = self._check_t1()
        self.results[Constants.CLASS_S] = self._check_s()
        self.results[Constants.CLASS_M] = self._check_m()
        self.results[Constants.CLASS_L] = self._check_l()

    def _check_t0(self) -> bool:
        """Проверка принадлежности к T0 (сохраняет 0)"""
        return self.truth_table[Constants.ZERO_INDEX][Constants.OUTPUT_KEY] == Constants.ZERO

    def _check_t1(self) -> bool:
        """Проверка принадлежности к T1 (сохраняет 1)"""
        return self.truth_table[-Constants.FIRST_INDEX][Constants.OUTPUT_KEY] == Constants.ONE

    def _check_s(self) -> bool:
        """Проверка самодвойственности"""
        n = len(self.truth_table)
        if n == Constants.ONE:
            return False
        for i in range(n // Constants.TWO):
            if self.truth_table[i][Constants.OUTPUT_KEY] == self.truth_table[n - Constants.ONE - i][Constants.OUTPUT_KEY]:
                return False
        return True

    def _check_m(self) -> bool:
        """Проверка монотонности"""
        n = len(self.variables)
        for i in range(len(self.truth_table)):
            for j in range(i + Constants.ONE, len(self.truth_table)):
                le = all(self.truth_table[i][Constants.INPUTS_KEY][k] <= self.truth_table[j][Constants.INPUTS_KEY][k]
                         for k in range(n))
                if le and self.truth_table[i][Constants.OUTPUT_KEY] > self.truth_table[j][Constants.OUTPUT_KEY]:
                    return False
        return True

    def _check_l(self) -> bool:
        """Проверка линейности"""
        values = [row[Constants.OUTPUT_KEY] for row in self.truth_table]
        coefficients = self._build_zhegalkin_coefficients(values)

        n = len(self.variables)
        for mask in range(Constants.POWER_BASE ** n):
            if bin(mask).count(Constants.BINARY_ONE) > Constants.ONE and coefficients[mask] != Constants.ZERO:
                return False
        return True

    def _build_zhegalkin_coefficients(self, values: list) -> list:
        """Построение коэффициентов полинома Жегалкина (метод треугольника)"""
        size = len(values)
        coefficients = values.copy()

        for i in range(size):
            for j in range(i):
                if (j & i) == j:
                    coefficients[i] ^= coefficients[j]

        return coefficients

    def get_results(self) -> dict:
        """Получение результатов"""
        return self.results

    def print_results(self):
        """Вывод результатов"""
        print("\nПринадлежность к классам Поста:")
        class_names = {
            Constants.CLASS_T0: 'T0 (сохраняет 0)',
            Constants.CLASS_T1: 'T1 (сохраняет 1)',
            Constants.CLASS_L: 'L (линейная)',
            Constants.CLASS_M: 'M (монотонная)',
            Constants.CLASS_S: 'S (самодвойственная)'
        }

        order = [Constants.CLASS_T0, Constants.CLASS_T1, Constants.CLASS_L,
                 Constants.CLASS_M, Constants.CLASS_S]

        print("\nT0\tT1\tL\tM\tS")
        symbols = []
        for class_id in order:
            symbols.append("+" if self.results[class_id] else "-")
        print("\t".join(symbols))
