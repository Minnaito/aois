from constants import *

class HashCell:
    """Структура ячейки хеш-таблицы согласно формату лабораторной работы."""

    def __init__(self) -> None:
        self.id: str = ""
        self.c: int = ZERO
        self.u: int = ZERO
        self.t: int = ZERO
        self.l: int = ZERO
        self.d: int = ZERO
        self.po: int = MINUS_ONE
        self.pi: str = ""

    def clear(self) -> None:
        """Полная очистка ячейки (освобождение)."""
        self.id = ""
        self.c = ZERO
        self.u = ZERO
        self.t = ZERO
        self.l = ZERO
        self.d = ZERO
        self.po = MINUS_ONE
        self.pi = ""