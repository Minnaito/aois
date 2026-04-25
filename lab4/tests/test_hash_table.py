"""
Unit-тесты для класса HashTable.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

import unittest
from src.hash_table import HashTable
from src.constants import TABLE_SIZE


class TestHashTableInsert(unittest.TestCase):
    """Тесты вставки записей."""

    def setUp(self) -> None:
        self.ht = HashTable()

    def test_insert_single(self) -> None:
        result = self.ht.insert("ген", "данные")
        self.assertTrue(result)
        self.assertEqual(self.ht.search("ген"), "данные")
        self.assertEqual(self.ht.fill_ratio(), 1 / TABLE_SIZE)

    def test_insert_multiple(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("ядро", "д2")
        self.ht.insert("клетка", "д3")
        self.assertEqual(self.ht.search("ген"), "д1")
        self.assertEqual(self.ht.search("ядро"), "д2")
        self.assertEqual(self.ht.search("клетка"), "д3")

    def test_insert_duplicate(self) -> None:
        self.ht.insert("ген", "д1")
        result = self.ht.insert("ген", "д2")
        self.assertFalse(result)
        self.assertEqual(self.ht.search("ген"), "д1")

    def test_insert_collision(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("генетика", "д2")
        self.ht.insert("гемоглобин", "д3")
        self.assertEqual(self.ht.search("ген"), "д1")
        self.assertEqual(self.ht.search("генетика"), "д2")
        self.assertEqual(self.ht.search("гемоглобин"), "д3")
        h = self.ht.hash_func("ген")
        self.assertEqual(self.ht.table[h].c, 0)
        c1_count = sum(1 for c in self.ht.table if c.u == 1 and c.d == 0 and c.c == 1)
        self.assertEqual(c1_count, 2)

    def test_insert_long_data(self) -> None:
        long_data = "A" * 50
        self.ht.insert("ген", long_data)
        h = self.ht.hash_func("ген")
        self.assertEqual(self.ht.table[h].l, 1)
        self.assertEqual(self.ht.search("ген"), long_data)

    def test_insert_short_data(self) -> None:
        short_data = "короткие"
        self.ht.insert("ген", short_data)
        h = self.ht.hash_func("ген")
        self.assertEqual(self.ht.table[h].l, 0)
        self.assertEqual(self.ht.search("ген"), short_data)


class TestHashTableSearch(unittest.TestCase):
    """Тесты поиска."""

    def setUp(self) -> None:
        self.ht = HashTable()
        self.ht.insert("ген", "д1")
        self.ht.insert("генетика", "д2")
        self.ht.insert("ядро", "д3")

    def test_search_existing(self) -> None:
        self.assertEqual(self.ht.search("ген"), "д1")
        self.assertEqual(self.ht.search("генетика"), "д2")
        self.assertEqual(self.ht.search("ядро"), "д3")

    def test_search_nonexistent(self) -> None:
        self.assertIsNone(self.ht.search("митоз"))

    def test_search_empty_string(self) -> None:
        self.assertIsNone(self.ht.search(""))

    def test_search_short_key(self) -> None:
        self.assertIsNone(self.ht.search("г"))

    def test_search_invalid_chars(self) -> None:
        self.assertIsNone(self.ht.search("123"))
        self.assertIsNone(self.ht.search("ab"))

    def test_search_in_chain(self) -> None:
        self.assertEqual(self.ht.search("ген"), "д1")
        self.assertEqual(self.ht.search("генетика"), "д2")


class TestHashTableUpdate(unittest.TestCase):
    """Тесты обновления."""

    def setUp(self) -> None:
        self.ht = HashTable()
        self.ht.insert("ген", "старое")
        self.ht.insert("генетика", "д2")

    def test_update_existing(self) -> None:
        self.assertTrue(self.ht.update("ген", "новое"))
        self.assertEqual(self.ht.search("ген"), "новое")

    def test_update_nonexistent(self) -> None:
        self.assertFalse(self.ht.update("митоз", "д"))

    def test_update_in_chain(self) -> None:
        self.assertTrue(self.ht.update("генетика", "новое цепи"))
        self.assertEqual(self.ht.search("генетика"), "новое цепи")

    def test_update_to_long(self) -> None:
        self.ht.update("ген", "B" * 40)
        h = self.ht.hash_func("ген")
        self.assertEqual(self.ht.table[h].l, 1)
        self.assertEqual(self.ht.search("ген"), "B" * 40)

    def test_update_to_short(self) -> None:
        self.ht.update("ген", "B" * 40)
        self.ht.update("ген", "короткое")
        h = self.ht.hash_func("ген")
        self.assertEqual(self.ht.table[h].l, 0)
        self.assertEqual(self.ht.search("ген"), "короткое")


class TestHashTableDelete(unittest.TestCase):
    """Тесты удаления."""

    def setUp(self) -> None:
        self.ht = HashTable()

    def test_delete_single(self) -> None:
        self.ht.insert("ядро", "д")
        self.ht.delete("ядро")
        self.assertIsNone(self.ht.search("ядро"))
        h = self.ht.hash_func("ядро")
        self.assertEqual(self.ht.table[h].d, 1)
        self.assertEqual(self.ht.table[h].u, 1)

    def test_delete_nonexistent(self) -> None:
        self.assertFalse(self.ht.delete("митоз"))

    def test_delete_last_in_chain(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("генетика", "д2")
        self.ht.insert("гемоглобин", "д3")
        self.ht.delete("гемоглобин")
        self.assertIsNone(self.ht.search("гемоглобин"))
        self.assertEqual(self.ht.search("ген"), "д1")
        self.assertEqual(self.ht.search("генетика"), "д2")

    def test_delete_middle_in_chain(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("генетика", "д2")
        self.ht.insert("гемоглобин", "д3")
        self.ht.delete("генетика")
        self.assertIsNone(self.ht.search("генетика"))
        self.assertEqual(self.ht.search("ген"), "д1")
        self.assertEqual(self.ht.search("гемоглобин"), "д3")

    def test_delete_first_in_chain(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("генетика", "д2")
        self.ht.insert("гемоглобин", "д3")
        self.ht.delete("ген")
        self.assertIsNone(self.ht.search("ген"))
        self.assertEqual(self.ht.search("генетика"), "д2")
        self.assertEqual(self.ht.search("гемоглобин"), "д3")

    def test_delete_updates_count(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("ядро", "д2")
        self.ht.delete("ген")
        self.assertEqual(self.ht.fill_ratio(), 1 / TABLE_SIZE)

    def test_reinsert_after_delete(self) -> None:
        self.ht.insert("ядро", "д1")
        self.ht.delete("ядро")
        self.ht.insert("ядро", "д2")
        self.assertEqual(self.ht.search("ядро"), "д2")

    def test_delete_all_in_chain(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("генетика", "д2")
        self.ht.insert("гемоглобин", "д3")
        self.ht.delete("гемоглобин")
        self.ht.delete("генетика")
        self.ht.delete("ген")
        self.assertIsNone(self.ht.search("ген"))
        self.assertIsNone(self.ht.search("генетика"))
        self.assertIsNone(self.ht.search("гемоглобин"))
        self.assertEqual(self.ht.fill_ratio(), 0.0)


class TestHashTableFillRatio(unittest.TestCase):
    """Тесты коэффициента заполнения."""

    def setUp(self) -> None:
        self.ht = HashTable()

    def test_empty(self) -> None:
        self.assertEqual(self.ht.fill_ratio(), 0.0)

    def test_after_insert(self) -> None:
        self.ht.insert("ген", "д")
        self.assertEqual(self.ht.fill_ratio(), 1 / TABLE_SIZE)
        self.ht.insert("ядро", "д")
        self.assertEqual(self.ht.fill_ratio(), 2 / TABLE_SIZE)

    def test_after_delete(self) -> None:
        self.ht.insert("ген", "д")
        self.ht.insert("ядро", "д")
        self.ht.delete("ген")
        self.assertEqual(self.ht.fill_ratio(), 1 / TABLE_SIZE)


class TestHashTableDisplay(unittest.TestCase):
    """Тесты display."""

    def setUp(self) -> None:
        self.ht = HashTable()

    def test_display_empty(self) -> None:
        try:
            self.ht.display()
        except Exception as e:
            self.fail(f"display() raised {type(e).__name__}")

    def test_display_with_data(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("генетика", "д2")
        try:
            self.ht.display()
        except Exception as e:
            self.fail(f"display() raised {type(e).__name__}")

    def test_display_with_deleted(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.delete("ген")
        try:
            self.ht.display()
        except Exception as e:
            self.fail(f"display() raised {type(e).__name__}")

    def test_display_with_long_data(self) -> None:
        self.ht.insert("ген", "A" * 100)
        try:
            self.ht.display()
        except Exception as e:
            self.fail(f"display() raised {type(e).__name__}")


class TestHashTableEdgeCases(unittest.TestCase):
    """Тесты граничных случаев."""

    def setUp(self) -> None:
        self.ht = HashTable()

    def test_insert_invalid_key_short(self) -> None:
        result = self.ht.insert("г", "данные")
        self.assertFalse(result)

    def test_insert_invalid_key_empty(self) -> None:
        result = self.ht.insert("", "данные")
        self.assertFalse(result)

    def test_insert_invalid_key_english(self) -> None:
        result = self.ht.insert("gene", "данные")
        self.assertFalse(result)

    def test_insert_invalid_key_digits(self) -> None:
        result = self.ht.insert("123", "данные")
        self.assertFalse(result)

    def test_update_invalid_key(self) -> None:
        self.assertFalse(self.ht.update("", "данные"))
        self.assertFalse(self.ht.update("a", "данные"))
        self.assertFalse(self.ht.update("12", "данные"))

    def test_update_nonexistent_key(self) -> None:
        self.assertFalse(self.ht.update("ген", "данные"))

    def test_delete_invalid_key(self) -> None:
        self.assertFalse(self.ht.delete(""))
        self.assertFalse(self.ht.delete("a"))
        self.assertFalse(self.ht.delete("12"))

    def test_delete_nonexistent_key(self) -> None:
        self.assertFalse(self.ht.delete("ген"))

    def test_compute_v_direct_call(self) -> None:
        self.assertEqual(self.ht.compute_v("ген"), 104)

    def test_hash_func_direct_call(self) -> None:
        self.assertEqual(self.ht.hash_func("ген"), 4)

    def test_is_valid_key_via_search(self) -> None:
        self.ht.insert("ген", "д1")
        self.assertIsNotNone(self.ht.search("ген"))
        self.assertIsNone(self.ht.search(""))
        self.assertIsNone(self.ht.search("г"))
        self.assertIsNone(self.ht.search("12"))

    def test_insert_after_logical_delete_reuses_cell(self) -> None:
        self.ht.insert("ядро", "д1")
        h_before = self.ht.hash_func("ядро")
        self.ht.delete("ядро")
        self.assertEqual(self.ht.table[h_before].d, 1)
        self.ht.insert("ядро", "д2")
        self.assertEqual(self.ht.table[h_before].d, 0)
        self.assertEqual(self.ht.table[h_before].u, 1)
        self.assertEqual(self.ht.search("ядро"), "д2")

    def test_display_with_mixed_content(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("ядро", "д2")
        self.ht.delete("ген")
        try:
            self.ht.display()
        except Exception as e:
            self.fail(f"display() raised {type(e).__name__}")

    def test_fill_ratio_after_reinsert(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("ядро", "д2")
        self.ht.delete("ген")
        self.assertEqual(self.ht.fill_ratio(), 1 / TABLE_SIZE)
        self.ht.insert("ген", "д3")
        self.assertEqual(self.ht.fill_ratio(), 2 / TABLE_SIZE)


class TestHashTableCollisionChain(unittest.TestCase):
    """Тесты цепочек коллизий."""

    def setUp(self) -> None:
        self.ht = HashTable()

    def test_chain_terminal_flags(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("генетика", "д2")
        self.ht.insert("гемоглобин", "д3")
        h = self.ht.hash_func("ген")
        self.assertEqual(self.ht.table[h].t, 0)
        curr = h
        while self.ht.table[curr].po != -1:
            curr = self.ht.table[curr].po
        self.assertEqual(self.ht.table[curr].t, 1)

    def test_chain_c_flags(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("генетика", "д2")
        self.ht.insert("гемоглобин", "д3")
        h = self.ht.hash_func("ген")
        self.assertEqual(self.ht.table[h].c, 0)
        curr = self.ht.table[h].po
        while curr != -1:
            self.assertEqual(self.ht.table[curr].c, 1)
            curr = self.ht.table[curr].po

    def test_chain_links(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("генетика", "д2")
        self.ht.insert("гемоглобин", "д3")
        h = self.ht.hash_func("ген")
        chain = []
        curr = h
        while curr != -1:
            cell = self.ht.table[curr]
            if cell.u == 1 and cell.d == 0:
                chain.append(cell.id)
            curr = cell.po
        self.assertEqual(len(chain), 3)
        self.assertIn("ген", chain)
        self.assertIn("генетика", chain)
        self.assertIn("гемоглобин", chain)

    def test_insert_fourth_collision(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("генетика", "д2")
        self.ht.insert("гемоглобин", "д3")
        result = self.ht.insert("гелий", "д4")
        self.assertTrue(result)
        self.assertEqual(self.ht.search("гелий"), "д4")

    def test_delete_all_chain_one_by_one(self) -> None:
        self.ht.insert("ген", "д1")
        self.ht.insert("генетика", "д2")
        self.ht.insert("гемоглобин", "д3")
        self.ht.insert("гелий", "д4")
        self.ht.delete("гелий")
        self.ht.delete("гемоглобин")
        self.ht.delete("генетика")
        self.ht.delete("ген")
        self.assertEqual(self.ht.fill_ratio(), 0.0)
        for key in ["ген", "генетика", "гемоглобин", "гелий"]:
            self.assertIsNone(self.ht.search(key))


class TestHashTableOverflow(unittest.TestCase):
    """Тесты области переполнения."""

    def setUp(self) -> None:
        self.ht = HashTable()

    def test_long_data_stored_in_overflow(self) -> None:
        long_data = "Б" * 40
        self.ht.insert("ген", long_data)
        h = self.ht.hash_func("ген")
        self.assertEqual(self.ht.table[h].l, 1)
        self.assertIn("&overflow", self.ht.table[h].pi)
        self.assertEqual(self.ht.search("ген"), long_data)

    def test_update_long_to_short(self) -> None:
        self.ht.insert("ген", "А" * 40)
        h = self.ht.hash_func("ген")
        self.assertEqual(self.ht.table[h].l, 1)
        self.ht.update("ген", "короткие")
        self.assertEqual(self.ht.table[h].l, 0)
        self.assertEqual(self.ht.table[h].pi, "короткие")

    def test_update_short_to_long(self) -> None:
        self.ht.insert("ген", "короткие")
        h = self.ht.hash_func("ген")
        self.assertEqual(self.ht.table[h].l, 0)
        self.ht.update("ген", "Б" * 40)
        self.assertEqual(self.ht.table[h].l, 1)
        self.assertEqual(self.ht.search("ген"), "Б" * 40)

    def test_delete_long_data_clears_overflow(self) -> None:
        self.ht.insert("ген", "А" * 40)
        h = self.ht.hash_func("ген")
        self.ht.delete("ген")
        self.assertFalse(self.ht.overflow.has(h))
        self.assertIsNone(self.ht.search("ген"))


class TestHashTableProbing(unittest.TestCase):
    """Тесты квадратичного пробинга."""

    def setUp(self) -> None:
        self.ht = HashTable()

    def test_quadratic_probing_indices(self) -> None:
        self.ht.insert("ген", "д1")          # индекс 4
        self.ht.insert("генетика", "д2")     # индекс 5 (4+1)
        self.ht.insert("гемоглобин", "д3")   # индекс 8 (4+4)
        self.ht.insert("гелий", "д4")        # индекс 13 (4+9)
        self.ht.insert("гербарий", "д5")     # индекс 0 (4+16=20→0)
        self.assertEqual(self.ht.search("ген"), "д1")
        self.assertEqual(self.ht.search("генетика"), "д2")
        self.assertEqual(self.ht.search("гемоглобин"), "д3")
        self.assertEqual(self.ht.search("гелий"), "д4")
        self.assertEqual(self.ht.search("гербарий"), "д5")

    def test_no_infinite_loop_on_full_table(self) -> None:
        prefixes = [
            "аб", "бв", "вг", "гд", "де", "еж", "жз", "зи", "ий", "кл",
            "лм", "мн", "но", "оп", "пр", "рс", "ст", "ту", "уф", "фх"
        ]
        for prefix in prefixes:
            self.ht.insert(prefix + "а", "д")
        result = self.ht.insert("хцч", "д")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()