from src.constants import Constants


class ExpressionValidator:
    """Валидатор логических выражений"""

    VALID_VARIABLES = set(Constants.VARIABLES[:Constants.FIVE])
    VALID_OPERATORS = {
        Constants.OP_AND,
        Constants.OP_OR,
        Constants.OP_NOT,
        Constants.OP_IMPL[Constants.ZERO],
        Constants.OP_IMPL[Constants.ONE],
        Constants.OP_EQUIV,
        Constants.PAREN_OPEN,
        Constants.PAREN_CLOSE
    }

    @classmethod
    def validate(cls, expression: str) -> bool:
        """Проверка корректности выражения"""
        if not expression:
            return False

        expr = expression.replace(' ', '')

        if not cls._check_characters(expr):
            return False

        if not cls._check_parentheses(expr):
            return False

        if not cls._check_operators(expr):
            return False

        return True

    @classmethod
    def _check_characters(cls, expr: str) -> bool:
        """Проверка допустимых символов"""
        i = Constants.ZERO
        while i < len(expr):
            char = expr[i]

            if char.isalpha():
                if char not in cls.VALID_VARIABLES:
                    return False
            elif char not in cls.VALID_OPERATORS and not char.isdigit():
                return False

            if char == Constants.OP_IMPL[Constants.ZERO] and i + Constants.ONE < len(expr) and expr[i + Constants.ONE] == Constants.OP_IMPL[Constants.ONE]:
                i += Constants.ONE

            i += Constants.ONE

        return True

    @classmethod
    def _check_parentheses(cls, expr: str) -> bool:
        """Проверка баланса скобок"""
        balance = Constants.ZERO
        for char in expr:
            if char == Constants.PAREN_OPEN:
                balance += Constants.ONE
            elif char == Constants.PAREN_CLOSE:
                balance -= Constants.ONE
                if balance < Constants.ZERO:
                    return False
        return balance == Constants.ZERO

    @classmethod
    def _check_operators(cls, expr: str) -> bool:
        """Проверка корректности использования операторов"""
        if expr.startswith((Constants.OP_AND, Constants.OP_OR, Constants.OP_EQUIV, Constants.OP_IMPL)):
            return False
        if expr.endswith((Constants.OP_AND, Constants.OP_OR, Constants.OP_NOT, Constants.OP_IMPL[Constants.ZERO], Constants.OP_EQUIV)):
            return False
        return True
