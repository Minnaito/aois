from src.constants import Constants


class DummyVariableFinder:
    """Поисковик фиктивных переменных"""

    def __init__(self, truth_table: list, variables: list):
        self.truth_table = truth_table
        self.variables = variables
        self.dummy_variables = []
        self._find_dummy_variables()

    def _find_dummy_variables(self):
        """Поиск фиктивных переменных"""
        n = len(self.variables)

        for i in range(n):
            if self._is_dummy(i):
                self.dummy_variables.append(self.variables[i])

    def _is_dummy(self, var_index: int) -> bool:
        """Проверка, является ли переменная фиктивной"""
        n = len(self.variables)
        groups = {}

        for row in self.truth_table:
            inputs = row['inputs']
            if len(inputs) != n:
                continue
            key = tuple(inputs[j] for j in range(n) if j != var_index)
            value = inputs[var_index]
            output = row['output']

            if key not in groups:
                groups[key] = {}
            groups[key][value] = output

        for key, outputs in groups.items():
            if 0 in outputs and 1 in outputs and outputs[0] != outputs[1]:
                return False

        return True

    def get_dummy_variables(self) -> list:
        """Получение списка фиктивных переменных"""
        return self.dummy_variables

    def print_results(self):
        """Вывод результатов"""
        if self.dummy_variables:
            print(Constants.format_error(Constants.MSG_DUMMY_FOUND,
                                        vars=', '.join(self.dummy_variables)))
            print(Constants.MSG_DUMMY_DESC)
        else:
            print(Constants.MSG_NO_DUMMY)
            print(Constants.MSG_ALL_VARS_ESSENTIAL)