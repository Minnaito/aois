"""
Unit-тесты для функций хеширования из hash_utils.py.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

import unittest
from src.hash_utils import char_value, compute_v, compute_h


class TestCharValue(unittest.TestCase):
    """Тесты для char_value."""

    def test_a(self) -> None:
        self.assertEqual(char_value('а'), 0)
        self.assertEqual(char_value('А'), 0)

    def test_ya(self) -> None:
        self.assertEqual(char_value('я'), 32)
        self.assertEqual(char_value('Я'), 32)

    def test_yo(self) -> None:
        self.assertEqual(char_value('ё'), 6)
        self.assertEqual(char_value('Ё'), 6)

    def test_middle(self) -> None:
        self.assertEqual(char_value('к'), 11)
        self.assertEqual(char_value('п'), 16)

    def test_invalid(self) -> None:
        self.assertEqual(char_value('a'), -1)
        self.assertEqual(char_value('1'), -1)
        self.assertEqual(char_value(' '), -1)
        self.assertEqual(char_value('.'), -1)
        self.assertEqual(char_value(''), -1)


class TestComputeV(unittest.TestCase):
    """Тесты для compute_v."""

    def test_gen(self) -> None:
        # г=3, е=5 → 3*33+5 = 104
        self.assertEqual(compute_v("ген"), 104)
        self.assertEqual(compute_v("ГЕН"), 104)

    def test_yadro(self) -> None:
        self.assertEqual(compute_v("ядро"), 1060)

    def test_ab(self) -> None:
        self.assertEqual(compute_v("аб"), 1)

    def test_same_first_letters(self) -> None:
        v1 = compute_v("ген")
        v2 = compute_v("генетика")
        v3 = compute_v("гемоглобин")
        self.assertEqual(v1, v2)
        self.assertEqual(v1, v3)

    def test_different_first_letters(self) -> None:
        self.assertNotEqual(compute_v("ген"), compute_v("клетка"))

    def test_too_short(self) -> None:
        with self.assertRaises(ValueError):
            compute_v("г")
        with self.assertRaises(ValueError):
            compute_v("")

    def test_invalid_raises(self) -> None:
        with self.assertRaises(ValueError):
            compute_v("g1")
        with self.assertRaises(ValueError):
            compute_v("1а")


class TestComputeH(unittest.TestCase):
    """Тесты для compute_h."""

    def test_basic(self) -> None:
        self.assertEqual(compute_h("ген", 20, 0), 4)

    def test_with_offset(self) -> None:
        self.assertEqual(compute_h("ген", 20, 100), 104)

    def test_size_affects(self) -> None:
        h1 = compute_h("белок", 10, 0)
        h2 = compute_h("белок", 20, 0)
        self.assertNotEqual(h1, h2)

    def test_same_v_same_h(self) -> None:
        h1 = compute_h("ген", 20, 0)
        h2 = compute_h("генетика", 20, 0)
        self.assertEqual(h1, h2)

    def test_within_bounds(self) -> None:
        keys = ["ген", "ядро", "клетка", "белок", "митоз", "рибосома"]
        for key in keys:
            for size in [10, 20, 50]:
                for base in [0, 100, 1000]:
                    h = compute_h(key, size, base)
                    self.assertGreaterEqual(h, base)
                    self.assertLess(h, base + size)


if __name__ == "__main__":
    unittest.main()