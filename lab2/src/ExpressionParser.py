import re
from typing import List, Dict
from abc import ABC, abstractmethod

from src.constants import Constants


class IExpressionParser(ABC):
    @abstractmethod
    def extract_variables(self, expression: str) -> List[str]:
        pass

    @abstractmethod
    def evaluate(self, expression: str, values: Dict[str, int]) -> int:
        pass

    @abstractmethod
    def validate_expression(self, expression: str) -> bool:
        pass


class BooleanExpressionParser(IExpressionParser):
    VALID_VARIABLES = set(Constants.VARIABLES[:Constants.FIVE])

    def extract_variables(self, expression: str) -> List[str]:
        vars_found = set(re.findall(r'[a-e]', expression))
        return sorted(list(vars_found))

    def evaluate(self, expression: str, values: Dict[str, int]) -> int:
        expr = expression.replace(' ', '')
        if expr == Constants.DEFAULT_OUTPUT_ZERO:
            return Constants.ZERO
        if expr == Constants.DEFAULT_OUTPUT_ONE:
            return Constants.ONE

        # Подставляем значения переменных
        for var, val in values.items():
            expr = expr.replace(var, str(val))

        tokens = self._tokenize(expr)
        self._tokens = tokens
        self._pos = Constants.ZERO
        return self._parse_expression()

    def _tokenize(self, expr: str) -> List[str]:
        tokens = []
        i = Constants.ZERO
        while i < len(expr):
            if expr[i] in Constants.BINARY_ZERO + Constants.BINARY_ONE:
                tokens.append(expr[i])
                i += Constants.ONE
            elif expr[i] in '()!&|~':
                tokens.append(expr[i])
                i += Constants.ONE
            elif expr[i] == Constants.SEPARATOR[Constants.ZERO] and i + Constants.ONE < len(expr) and expr[i + Constants.ONE] == '>':
                tokens.append(Constants.OP_IMPL)
                i += Constants.TWO
            elif expr[i] in 'abcde':
                tokens.append(expr[i])
                i += Constants.ONE
            else:
                raise ValueError(f"Недопустимый символ: {expr[i]}")
        return tokens

    def _peek(self) -> str:
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return ''

    def _consume(self, expected: str = None):
        if expected and self._peek() != expected:
            raise ValueError(f"Ожидалось '{expected}', получено '{self._peek()}'")
        self._pos += Constants.ONE


    def _parse_expression(self) -> int:
        return self._parse_equiv()

    def _parse_equiv(self) -> int:
        left = self._parse_impl()
        while self._peek() == Constants.OP_EQUIV:
            self._consume(Constants.OP_EQUIV)
            right = self._parse_impl()
            left = Constants.ONE if left == right else Constants.ZERO
        return left

    def _parse_impl(self) -> int:
        left = self._parse_disj()
        while self._peek() == Constants.OP_IMPL:
            self._consume(Constants.OP_IMPL)
            right = self._parse_disj()
            left = (Constants.ONE - left) | right
        return left

    def _parse_disj(self) -> int:
        left = self._parse_conj()
        while self._peek() == Constants.OP_OR:
            self._consume(Constants.OP_OR)
            right = self._parse_conj()
            left = left | right
        return left

    def _parse_conj(self) -> int:
        left = self._parse_unary()
        while self._peek() == Constants.OP_AND:
            self._consume(Constants.OP_AND)
            right = self._parse_unary()
            left = left & right
        return left

    def _parse_unary(self) -> int:
        if self._peek() == Constants.OP_NOT:
            self._consume(Constants.OP_NOT)
            return Constants.ONE - self._parse_unary()
        return self._parse_primary()

    def _parse_primary(self) -> int:
        token = self._peek()
        if token == Constants.DEFAULT_OUTPUT_ZERO:
            self._consume()
            return Constants.ZERO
        elif token == Constants.DEFAULT_OUTPUT_ONE:
            self._consume()
            return Constants.ONE
        elif token == Constants.PAREN_OPEN:
            self._consume(Constants.PAREN_OPEN)
            val = self._parse_expression()
            self._consume(Constants.PAREN_CLOSE)
            return val
        else:
            raise ValueError(f"Неожиданный токен: {token}")

    def validate_expression(self, expression: str) -> bool:
        if not expression:
            return False
        expr = expression.replace(' ', '')
        if expr in [Constants.DEFAULT_OUTPUT_ZERO, Constants.DEFAULT_OUTPUT_ONE]:
            return True

        allowed = set('abcde' + Constants.BINARY_ZERO + Constants.BINARY_ONE + '!&|~->()')
        i = Constants.ZERO
        while i < len(expr):
            ch = expr[i]
            if ch == Constants.SEPARATOR[Constants.ZERO] and i + Constants.ONE < len(expr) and expr[i + Constants.ONE] == '>':
                i += Constants.TWO
                continue
            if ch not in allowed:
                return False
            i += Constants.ONE

        balance = Constants.ZERO
        for ch in expr:
            if ch == Constants.PAREN_OPEN:
                balance += Constants.ONE
            elif ch == Constants.PAREN_CLOSE:
                balance -= Constants.ONE
                if balance < Constants.ZERO:
                    return False
        if balance != Constants.ZERO:
            return False

        test_expr = re.sub(r'[a-e]', Constants.DEFAULT_OUTPUT_ONE, expr)
        try:
            tokens = self._tokenize(test_expr)
            self._tokens = tokens
            self._pos = Constants.ZERO
            self._parse_expression()
            return self._pos == len(tokens)
        except (ValueError, IndexError):
            return False
