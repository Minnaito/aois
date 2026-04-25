class OverflowManager:
    """Хранит данные, которые не поместились в основную таблицу."""

    def __init__(self) -> None:
        self._storage: dict[int, str] = {}

    def put(self, index: int, data: str) -> None:
        """Сохранить данные для ячейки с указанным индексом."""
        self._storage[index] = data

    def get(self, index: int) -> str | None:
        """Получить данные для ячейки."""
        return self._storage.get(index)

    def remove(self, index: int) -> None:
        """Удалить данные для ячейки."""
        self._storage.pop(index, None)

    def has(self, index: int) -> bool:
        """Проверить, есть ли данные в переполнении для индекса."""
        return index in self._storage