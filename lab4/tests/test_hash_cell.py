"""
Unit-тесты для класса HashCell.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

import unittest
from src.hash_cell import HashCell


class TestHashCell(unittest.TestCase):
    """Тесты для HashCell."""

    def test_default_values(self) -> None:
        """Проверка значений по умолчанию."""
        cell = HashCell()
        self.assertEqual(cell.id, "")
        self.assertEqual(cell.c, 0)
        self.assertEqual(cell.u, 0)
        self.assertEqual(cell.t, 0)
        self.assertEqual(cell.l, 0)
        self.assertEqual(cell.d, 0)
        self.assertEqual(cell.po, -1)
        self.assertEqual(cell.pi, "")

    def test_set_values(self) -> None:
        """Проверка установки значений полей."""
        cell = HashCell()
        cell.id = "ген"
        cell.c = 1
        cell.u = 1
        cell.t = 1
        cell.l = 0
        cell.d = 0
        cell.po = 5
        cell.pi = "данные"

        self.assertEqual(cell.id, "ген")
        self.assertEqual(cell.c, 1)
        self.assertEqual(cell.u, 1)
        self.assertEqual(cell.t, 1)
        self.assertEqual(cell.l, 0)
        self.assertEqual(cell.d, 0)
        self.assertEqual(cell.po, 5)
        self.assertEqual(cell.pi, "данные")

    def test_clear(self) -> None:
        """Проверка полной очистки ячейки."""
        cell = HashCell()
        cell.id = "ген"
        cell.c = 1
        cell.u = 1
        cell.t = 1
        cell.l = 1
        cell.d = 1
        cell.po = 5
        cell.pi = "данные"

        cell.clear()

        self.assertEqual(cell.id, "")
        self.assertEqual(cell.c, 0)
        self.assertEqual(cell.u, 0)
        self.assertEqual(cell.t, 0)
        self.assertEqual(cell.l, 0)
        self.assertEqual(cell.d, 0)
        self.assertEqual(cell.po, -1)
        self.assertEqual(cell.pi, "")

    def test_multiple_cells_independent(self) -> None:
        """Проверка независимости ячеек."""
        cell1 = HashCell()
        cell2 = HashCell()

        cell1.id = "ген"
        cell1.u = 1
        cell1.pi = "данные1"

        cell2.id = "ядро"
        cell2.u = 1
        cell2.pi = "данные2"

        self.assertEqual(cell1.id, "ген")
        self.assertEqual(cell2.id, "ядро")
        self.assertNotEqual(cell1.id, cell2.id)

    def test_po_default(self) -> None:
        """Проверка, что Po по умолчанию -1."""
        cell = HashCell()
        self.assertEqual(cell.po, -1)

    def test_po_positive(self) -> None:
        """Проверка установки Po в положительное значение."""
        cell = HashCell()
        cell.po = 10
        self.assertEqual(cell.po, 10)

    def test_po_zero(self) -> None:
        """Проверка установки Po в 0."""
        cell = HashCell()
        cell.po = 0
        self.assertEqual(cell.po, 0)

    def test_d_flag(self) -> None:
        """Проверка флага удаления."""
        cell = HashCell()
        self.assertEqual(cell.d, 0)
        cell.d = 1
        self.assertEqual(cell.d, 1)
        cell.d = 0
        self.assertEqual(cell.d, 0)

    def test_l_flag(self) -> None:
        """Проверка флага связи данных."""
        cell = HashCell()
        self.assertEqual(cell.l, 0)
        cell.l = 1
        self.assertEqual(cell.l, 1)

    def test_t_flag(self) -> None:
        """Проверка терминального флага."""
        cell = HashCell()
        self.assertEqual(cell.t, 0)
        cell.t = 1
        self.assertEqual(cell.t, 1)

    def test_c_flag(self) -> None:
        """Проверка флага коллизии."""
        cell = HashCell()
        self.assertEqual(cell.c, 0)
        cell.c = 1
        self.assertEqual(cell.c, 1)

    def test_all_fields_together(self) -> None:
        """Проверка всех полей одновременно после изменений."""
        cell = HashCell()
        cell.id = "тест"
        cell.c = 1
        cell.u = 1
        cell.t = 0
        cell.l = 1
        cell.d = 0
        cell.po = 7
        cell.pi = "&overflow[7]"

        self.assertEqual(cell.id, "тест")
        self.assertEqual(cell.c, 1)
        self.assertEqual(cell.u, 1)
        self.assertEqual(cell.t, 0)
        self.assertEqual(cell.l, 1)
        self.assertEqual(cell.d, 0)
        self.assertEqual(cell.po, 7)
        self.assertEqual(cell.pi, "&overflow[7]")

    def test_clear_then_reuse(self) -> None:
        """Очистка и повторное использование ячейки."""
        cell = HashCell()
        cell.id = "старое"
        cell.u = 1
        cell.pi = "данные"
        cell.clear()
        cell.id = "новое"
        cell.u = 1
        cell.pi = "новые данные"
        self.assertEqual(cell.id, "новое")
        self.assertEqual(cell.u, 1)
        self.assertEqual(cell.pi, "новые данные")


if __name__ == "__main__":
    unittest.main()
