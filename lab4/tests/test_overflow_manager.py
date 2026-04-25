"""
Unit-тесты для класса OverflowManager.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

import unittest
from src.overflow_manager import OverflowManager


class TestOverflowManager(unittest.TestCase):
    """Тесты для OverflowManager."""

    def setUp(self) -> None:
        self.om = OverflowManager()

    def test_put_and_get(self) -> None:
        self.om.put(0, "данные")
        self.assertEqual(self.om.get(0), "данные")

    def test_get_nonexistent(self) -> None:
        self.assertIsNone(self.om.get(999))

    def test_has_existing(self) -> None:
        self.om.put(5, "данные")
        self.assertTrue(self.om.has(5))

    def test_has_nonexistent(self) -> None:
        self.assertFalse(self.om.has(10))

    def test_remove_existing(self) -> None:
        self.om.put(3, "данные")
        self.assertTrue(self.om.has(3))
        self.om.remove(3)
        self.assertFalse(self.om.has(3))
        self.assertIsNone(self.om.get(3))

    def test_remove_nonexistent_no_error(self) -> None:
        try:
            self.om.remove(999)
        except Exception as e:
            self.fail(f"remove() raised {type(e).__name__} unexpectedly!")

    def test_overwrite(self) -> None:
        self.om.put(1, "старые")
        self.om.put(1, "новые")
        self.assertEqual(self.om.get(1), "новые")

    def test_multiple_indices(self) -> None:
        self.om.put(0, "д0")
        self.om.put(5, "д5")
        self.om.put(13, "д13")
        self.assertEqual(self.om.get(0), "д0")
        self.assertEqual(self.om.get(5), "д5")
        self.assertEqual(self.om.get(13), "д13")

    def test_long_data(self) -> None:
        long_data = "A" * 1000
        self.om.put(7, long_data)
        self.assertEqual(self.om.get(7), long_data)
        self.assertEqual(len(self.om.get(7)), 1000)

    def test_empty_string(self) -> None:
        self.om.put(2, "")
        self.assertEqual(self.om.get(2), "")
        self.assertTrue(self.om.has(2))

    def test_remove_twice_no_error(self) -> None:
        """Двойное удаление не вызывает ошибку."""
        self.om.put(1, "данные")
        self.om.remove(1)
        try:
            self.om.remove(1)
        except Exception as e:
            self.fail(f"remove() raised {type(e).__name__} unexpectedly!")

    def test_has_after_remove(self) -> None:
        """После удаления has возвращает False."""
        self.om.put(1, "данные")
        self.om.remove(1)
        self.assertFalse(self.om.has(1))

    def test_get_after_remove(self) -> None:
        """После удаления get возвращает None."""
        self.om.put(1, "данные")
        self.om.remove(1)
        self.assertIsNone(self.om.get(1))

    def test_put_empty_then_overwrite(self) -> None:
        """Перезапись пустой строки."""
        self.om.put(1, "")
        self.assertEqual(self.om.get(1), "")
        self.om.put(1, "непусто")
        self.assertEqual(self.om.get(1), "непусто")


if __name__ == "__main__":
    unittest.main()