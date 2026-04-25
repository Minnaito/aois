from constants import *
from hash_cell import HashCell
from overflow_manager import OverflowManager
from hash_utils import compute_v, compute_h


class HashTable:
    """Хеш-таблица с внутренней адресацией и квадратичным пробингом."""

    def __init__(self, size: int = TABLE_SIZE) -> None:
        self.size: int = size
        self.table: list[HashCell] = [HashCell() for _ in range(size)]
        self.count: int = ZERO
        self.overflow: OverflowManager = OverflowManager()
        self._initial_address: int = INITIAL_ADDRESS

    def compute_v(self, key: str) -> int:
        return compute_v(key)

    def hash_func(self, key: str) -> int:
        return compute_h(key, self.size, self._initial_address)

    def _find_reusable_cell(self, h: int) -> int:
        """Квадратичный пробинг: сначала свободная (U=0), затем удалённая (D=1)."""
        for i in range(ONE, MAX_PROBING_ATTEMPTS + ONE):
            hi = (h + i * i) % self.size
            if self.table[hi].u == ZERO:
                return hi
        for i in range(ONE, MAX_PROBING_ATTEMPTS + ONE):
            hi = (h + i * i) % self.size
            cell = self.table[hi]
            if cell.u == ONE and cell.d == ONE:
                return hi
        return MINUS_ONE

    def _clear_cell(self, idx: int) -> None:
        """Полное освобождение ячейки."""
        self.overflow.remove(idx)
        self.table[idx].clear()

    def _is_data_long(self, data: str) -> bool:
        return len(data) > MAX_DATA_LENGTH

    def _store_data(self, idx: int, data: str) -> None:
        """Сохраняет данные в ячейку или в overflow."""
        cell = self.table[idx]
        if self._is_data_long(data):
            self.overflow.put(idx, data)
            cell.pi = f"&overflow[{idx}]"
            cell.l = ONE
        else:
            self.overflow.remove(idx)
            cell.pi = data
            cell.l = ZERO

    def _get_data(self, idx: int) -> str | None:
        """Извлекает данные из ячейки."""
        cell = self.table[idx]
        if cell.l == ONE:
            return self.overflow.get(idx)
        return cell.pi

    def _find_in_chain(self, key: str, h: int) -> tuple[int, int]:
        """Ищет ключ в цепочке, начиная с h."""
        curr = h
        prev = MINUS_ONE
        while curr != MINUS_ONE:
            cell = self.table[curr]
            if cell.u == ONE and cell.d == ZERO and cell.id == key:
                return curr, prev
            prev = curr
            curr = cell.po
        return MINUS_ONE, MINUS_ONE

    def _get_last_in_chain(self, h: int) -> tuple[int, int]:
        """Возвращает (индекс_последней_активной, индекс_предпоследней)."""
        curr = h
        prev = MINUS_ONE
        last = h
        last_prev = MINUS_ONE
        while curr != MINUS_ONE:
            cell = self.table[curr]
            if cell.u == ONE and cell.d == ZERO:
                last_prev = prev
                last = curr
            prev = curr
            curr = cell.po
        return last, last_prev

    def _is_valid_key(self, key: str) -> bool:
        """Проверяет, что ключ валиден (русские буквы, минимум 2)."""
        if not key or len(key) < MIN_KEY_LENGTH:
            return False
        return all('а' <= ch <= 'я' or ch == 'ё' for ch in key.lower())

    def insert(self, key: str, data: str) -> bool:
        """Вставка новой записи."""
        if not self._is_valid_key(key):
            print(f"Недопустимый ключ: '{key}'")
            return False

        if self.search(key) is not None:
            print(f"Ключ '{key}' уже существует.")
            return False

        h = self.hash_func(key)
        cell = self.table[h]

        if cell.u == ZERO or (cell.u == ONE and cell.d == ONE):
            if cell.d == ONE:
                self._clear_cell(h)
                cell = self.table[h]
            cell.id = key
            cell.c = ZERO
            cell.u = ONE
            cell.t = ONE
            cell.d = ZERO
            cell.po = MINUS_ONE
            self._store_data(h, data)
            self.count += ONE
            return True

        last_idx, _ = self._get_last_in_chain(h)
        free_idx = self._find_reusable_cell(h)
        if free_idx == MINUS_ONE:
            print("Переполнение хеш-таблицы.")
            return False

        free_cell = self.table[free_idx]
        if free_cell.u == ONE and free_cell.d == ONE:
            self._clear_cell(free_idx)
            free_cell = self.table[free_idx]

        free_cell.id = key
        free_cell.c = ONE
        free_cell.u = ONE
        free_cell.t = ONE
        free_cell.d = ZERO
        free_cell.po = MINUS_ONE
        self._store_data(free_idx, data)

        self.table[last_idx].po = free_idx
        self.table[last_idx].t = ZERO
        self.count += ONE
        return True

    def search(self, key: str) -> str | None:
        """Поиск данных по ключу."""
        if not self._is_valid_key(key):
            return None

        try:
            h = self.hash_func(key)
        except ValueError:
            return None

        idx, _ = self._find_in_chain(key, h)
        if idx == MINUS_ONE:
            return None
        return self._get_data(idx)

    def update(self, key: str, new_data: str) -> bool:
        """Обновление данных существующей записи."""
        if not self._is_valid_key(key):
            print(f"Недопустимый ключ: '{key}'")
            return False

        try:
            h = self.hash_func(key)
        except ValueError:
            print(f"Недопустимый ключ: '{key}'")
            return False

        idx, _ = self._find_in_chain(key, h)
        if idx == MINUS_ONE:
            print(f"Ключ '{key}' не найден.")
            return False
        self._store_data(idx, new_data)
        return True

    def delete(self, key: str) -> bool:
        """Удаление записи."""
        if not self._is_valid_key(key):
            print(f"Недопустимый ключ: '{key}'")
            return False

        try:
            h = self.hash_func(key)
        except ValueError:
            print(f"Недопустимый ключ: '{key}'")
            return False

        idx, prev_idx = self._find_in_chain(key, h)
        if idx == MINUS_ONE:
            print(f"Ключ '{key}' не найден.")
            return False

        cell = self.table[idx]

        if cell.po == MINUS_ONE:
            cell.d = ONE
            self.overflow.remove(idx)
            cell.pi = ""
            if prev_idx != MINUS_ONE:
                self.table[prev_idx].po = MINUS_ONE
                self.table[prev_idx].t = ONE
            self.count -= ONE
            return True

        next_idx = cell.po
        next_cell = self.table[next_idx]

        cell.id = next_cell.id
        cell.c = next_cell.c
        cell.u = next_cell.u
        cell.t = next_cell.t
        cell.l = next_cell.l
        cell.d = next_cell.d
        cell.pi = next_cell.pi
        cell.po = next_cell.po

        if self.overflow.has(next_idx):
            self.overflow.put(idx, self.overflow.get(next_idx))
            self.overflow.remove(next_idx)
        else:
            self.overflow.remove(idx)

        self._clear_cell(next_idx)
        self.count -= ONE
        return True

    def fill_ratio(self) -> float:
        """Коэффициент заполнения таблицы."""
        return self.count / self.size

    def display(self) -> None:
        """Вывод всей таблицы с хеш-данными."""
        print("=" * DISPLAY_LINE_LENGTH)
        header = (
            f"{'Ключ':<{COL_WIDTH_KEY}} {'V':<{COL_WIDTH_V}} {'h':<{COL_WIDTH_H}} | "
            f"{'Idx':<{COL_WIDTH_IDX}} {'ID':<{COL_WIDTH_ID}} {'C':<{COL_WIDTH_C}} {'U':<{COL_WIDTH_U}} {'T':<{COL_WIDTH_T}} "
            f"{'L':<{COL_WIDTH_L}} {'D':<{COL_WIDTH_D}} {'Po':<{COL_WIDTH_PO}} {'Pi'}"
        )
        print(header)
        print("-" * DISPLAY_LINE_LENGTH)

        for i, cell in enumerate(self.table):
            if cell.u == ZERO:
                print(
                    f"{'':<{COL_WIDTH_KEY}} {'':<{COL_WIDTH_V}} {'':<{COL_WIDTH_H}} | "
                    f"{i:<{COL_WIDTH_IDX}} {'':<{COL_WIDTH_ID}} {cell.c:<{COL_WIDTH_C}} {cell.u:<{COL_WIDTH_U}} {cell.t:<{COL_WIDTH_T}} "
                    f"{cell.l:<{COL_WIDTH_L}} {cell.d:<{COL_WIDTH_D}} {cell.po:<{COL_WIDTH_PO}} {cell.pi}"
                )
            elif cell.d == ONE:
                v = self.compute_v(cell.id)
                h = self.hash_func(cell.id)
                print(
                    f"{cell.id:<{COL_WIDTH_KEY}} {v:<{COL_WIDTH_V}} {h:<{COL_WIDTH_H}} | "
                    f"{i:<{COL_WIDTH_IDX}} {cell.id:<{COL_WIDTH_ID}} {cell.c:<{COL_WIDTH_C}} {cell.u:<{COL_WIDTH_U}} {cell.t:<{COL_WIDTH_T}} "
                    f"{cell.l:<{COL_WIDTH_L}} {cell.d:<{COL_WIDTH_D}} {cell.po:<{COL_WIDTH_PO}} [УДАЛЕНО]"
                )
            else:
                v = self.compute_v(cell.id)
                h = self.hash_func(cell.id)
                data_display = self._get_data(i) or cell.pi
                if len(data_display) > MAX_DATA_DISPLAY:
                    data_display = data_display[:MAX_DATA_DISPLAY] + "..."
                print(
                    f"{cell.id:<{COL_WIDTH_KEY}} {v:<{COL_WIDTH_V}} {h:<{COL_WIDTH_H}} | "
                    f"{i:<{COL_WIDTH_IDX}} {cell.id:<{COL_WIDTH_ID}} {cell.c:<{COL_WIDTH_C}} {cell.u:<{COL_WIDTH_U}} {cell.t:<{COL_WIDTH_T}} "
                    f"{cell.l:<{COL_WIDTH_L}} {cell.d:<{COL_WIDTH_D}} {cell.po:<{COL_WIDTH_PO}} {data_display}"
                )

        print("=" * DISPLAY_LINE_LENGTH)
        print(f"Коэффициент заполнения: {self.fill_ratio():.2f}")