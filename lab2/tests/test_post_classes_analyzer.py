import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.PostClassesAnalyzer import PostClassesAnalyzer
from src.TruthTableGenerator import TruthTableGenerator


class TestPostClassesAnalyzer(unittest.TestCase):
    """Тесты для PostClassesAnalyzer"""

    def test_and_t0(self):
        """Тест T0 для AND"""
        tt = TruthTableGenerator("a&b")
        analyzer = PostClassesAnalyzer(tt.get_truth_table(), tt.get_variables())
        results = analyzer.get_results()
        self.assertTrue(results['T0'])

    def test_and_t1(self):
        """Тест T1 для AND"""
        tt = TruthTableGenerator("a&b")
        analyzer = PostClassesAnalyzer(tt.get_truth_table(), tt.get_variables())
        results = analyzer.get_results()
        # AND: 1&1=1, значит T1=true
        self.assertTrue(results['T1'])

    def test_or_t0(self):
        """Тест T0 для OR"""
        tt = TruthTableGenerator("a|b")
        analyzer = PostClassesAnalyzer(tt.get_truth_table(), tt.get_variables())
        results = analyzer.get_results()
        # OR: 0|0=0, значит T0=true
        self.assertTrue(results['T0'])

    def test_or_t1(self):
        """Тест T1 для OR"""
        tt = TruthTableGenerator("a|b")
        analyzer = PostClassesAnalyzer(tt.get_truth_table(), tt.get_variables())
        results = analyzer.get_results()
        self.assertTrue(results['T1'])

    def test_not_self_dual(self):
        """Тест самодвойственности для NOT"""
        tt = TruthTableGenerator("!a")
        analyzer = PostClassesAnalyzer(tt.get_truth_table(), tt.get_variables())
        results = analyzer.get_results()
        self.assertTrue(results['S'])

    def test_and_self_dual(self):
        """Тест самодвойственности для AND"""
        tt = TruthTableGenerator("a&b")
        analyzer = PostClassesAnalyzer(tt.get_truth_table(), tt.get_variables())
        results = analyzer.get_results()
        self.assertFalse(results['S'])

    def test_and_monotone(self):
        """Тест монотонности для AND"""
        tt = TruthTableGenerator("a&b")
        analyzer = PostClassesAnalyzer(tt.get_truth_table(), tt.get_variables())
        results = analyzer.get_results()
        self.assertTrue(results['M'])

    def test_xor_monotone(self):
        """Тест монотонности для XOR"""
        tt = TruthTableGenerator("a^b")
        analyzer = PostClassesAnalyzer(tt.get_truth_table(), tt.get_variables())
        results = analyzer.get_results()
        self.assertFalse(results['M'])

    def test_xor_linear(self):
        """Тест линейности для XOR"""
        tt = TruthTableGenerator("a^b")
        analyzer = PostClassesAnalyzer(tt.get_truth_table(), tt.get_variables())
        results = analyzer.get_results()
        self.assertTrue(results['L'])

    def test_and_linear(self):
        """Тест линейности для AND"""
        tt = TruthTableGenerator("a&b")
        analyzer = PostClassesAnalyzer(tt.get_truth_table(), tt.get_variables())
        results = analyzer.get_results()
        self.assertFalse(results['L'])

    def test_constant_zero(self):
        """Тест константы 0"""
        tt = TruthTableGenerator("0")
        analyzer = PostClassesAnalyzer(tt.get_truth_table(), tt.get_variables())
        results = analyzer.get_results()
        self.assertTrue(results['T0'])
        self.assertFalse(results['T1'])
        self.assertTrue(results['M'])
        self.assertTrue(results['L'])

    def test_constant_one(self):
        """Тест константы 1"""
        tt = TruthTableGenerator("1")
        analyzer = PostClassesAnalyzer(tt.get_truth_table(), tt.get_variables())
        results = analyzer.get_results()
        self.assertFalse(results['T0'])
        self.assertTrue(results['T1'])
        self.assertTrue(results['M'])
        self.assertTrue(results['L'])


if __name__ == '__main__':
    unittest.main()