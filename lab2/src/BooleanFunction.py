from typing import Optional, Dict, Any
from .ExpressionParser import BooleanExpressionParser
from .TruthTable import TruthTable


class BooleanFunction:
    """Основная модель булевой функции"""

    def __init__(self, expression: str, parser: Optional[BooleanExpressionParser] = None):
        self.parser = parser or BooleanExpressionParser()

        if expression in ['0', '1']:
            self.expression = expression
            self.variables = []
            self.truth_table = TruthTable(self.variables, expression, self.parser)
            return

        if not self.parser.validate_expression(expression):
            raise ValueError(f"Некорректное выражение: {expression}")

        self.expression = expression
        self.variables = self.parser.extract_variables(expression)
        self.truth_table = TruthTable(self.variables, expression, self.parser)

    def get_variable_count(self) -> int:
        """Получить количество переменных"""
        return len(self.variables)

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            'expression': self.expression,
            'variables': self.variables,
            'truth_table': [(bits, result) for bits, result in self.truth_table]
        }
