from typing import List
from src.constants import Constants


class TermParser:
    """Парсер термов логических выражений"""

    def parse_term(self, term: str) -> List[str]:
        """Разбор терма на литералы"""
        term = term.strip(f'{Constants.PAREN_OPEN}{Constants.PAREN_CLOSE}')
        if Constants.OP_AND in term:
            return term.split(Constants.OP_AND)
        if Constants.OP_OR in term:
            return term.split(Constants.OP_OR)
        return [term]

    def parse_dnf(self, dnf: str) -> List[str]:
        """Разбор ДНФ на термы"""
        if Constants.OP_OR_SYMBOL in dnf:
            terms = dnf.split(f' {Constants.OP_OR_SYMBOL} ')
        elif Constants.OP_OR in dnf:
            terms = dnf.split(f' {Constants.OP_OR} ')
        else:
            terms = [dnf]

        return [t.strip(f'{Constants.PAREN_OPEN}{Constants.PAREN_CLOSE}') for t in terms]

    def join_literals(self, literals: List[str], operator: str) -> str:
        """Объединение литералов в терм"""
        if not literals:
            return ''
        if len(literals) == Constants.ONE:
            return literals[Constants.ZERO_INDEX]
        return f'{Constants.PAREN_OPEN}{operator.join(literals)}{Constants.PAREN_CLOSE}'

    def get_literal_variable(self, literal: str) -> str:
        """Получение переменной из литерала"""
        return literal.replace(Constants.OP_NOT, '')

    def is_negated(self, literal: str) -> bool:
        """Проверка, является ли литерал отрицанием"""
        return literal.startswith(Constants.OP_NOT)
