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
        # Первая строка таблицы - все переменные = 0
        return self.truth_table[0]['output'] == 0

    def _check_t1(self) -> bool:
        """Проверка принадлежности к T1 (сохраняет 1)"""
        # Последняя строка таблицы - все переменные = 1
        return self.truth_table[-1]['output'] == 1

    def _check_s(self) -> bool:
        """Проверка самодвойственности"""
        n = len(self.truth_table)
        for i in range(n // Constants.POWER_BASE):
            if self.truth_table[i]['output'] == self.truth_table[n - 1 - i]['output']:
                return False
        return True

    def _check_m(self) -> bool:
        """Проверка монотонности"""
        n = len(self.variables)
        for i in range(len(self.truth_table)):
            for j in range(i + 1, len(self.truth_table)):
                # Проверяем, что i <= j покомпонентно
                le = all(self.truth_table[i]['inputs'][k] <= self.truth_table[j]['inputs'][k]
                         for k in range(n))
                if le and self.truth_table[i]['output'] > self.truth_table[j]['output']:
                    return False
        return True

    def _check_l(self) -> bool:
        """Проверка линейности"""
        values = [row['output'] for row in self.truth_table]
        coefficients = self._build_zhegalkin_coefficients(values)

        n = len(self.variables)
        for mask in range(1 << n):
            if bin(mask).count(Constants.BINARY_ONE) > 1 and coefficients[mask] != 0:
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
            Constants.CLASS_S: 'S (самодвойственная)',
            Constants.CLASS_M: 'M (монотонная)',
            Constants.CLASS_L: 'L (линейная)'
        }

        for class_id, belongs in self.results.items():
            status = "✓ принадлежит" if belongs else "✗ не принадлежит"
            print(f"  {class_names[class_id]}: {status}")