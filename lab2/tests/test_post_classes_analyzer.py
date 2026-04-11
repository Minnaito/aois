import unittest
from src.PostClassesAnalyzer import PostClassesAnalyzer
from src.TruthTable import TruthTable
from src.ExpressionParser import BooleanExpressionParser
from src.constants import Constants


class TestPostClassesAnalyzer(unittest.TestCase):
    def setUp(self):
        self.parser = BooleanExpressionParser()

    def _analyze(self, expr, variables):
        tt = TruthTable(variables, expr, self.parser)
        truth_table_list = [{'inputs': bits, 'output': res} for bits, res in tt]
        return PostClassesAnalyzer(truth_table_list, variables)

    def test_t0_class(self):
        analyzer = self._analyze("a&b", ['a','b'])
        self.assertTrue(analyzer.results[Constants.CLASS_T0])
        analyzer = self._analyze("a|b", ['a','b'])
        self.assertTrue(analyzer.results[Constants.CLASS_T0])
        analyzer = self._analyze("!a", ['a'])
        self.assertFalse(analyzer.results[Constants.CLASS_T0])

    def test_t1_class(self):
        analyzer = self._analyze("a&b", ['a','b'])
        self.assertTrue(analyzer.results[Constants.CLASS_T1])
        analyzer = self._analyze("a~b", ['a','b'])
        self.assertTrue(analyzer.results[Constants.CLASS_T1])
        analyzer = self._analyze("!(a&b)", ['a','b'])
        self.assertFalse(analyzer.results[Constants.CLASS_T1])

    def test_check_s_for_constant(self):
        """Тест проверки самодвойственности для константы"""
        truth_table = [{'inputs': (), 'output': 0}]
        analyzer = PostClassesAnalyzer(truth_table, [])
        self.assertFalse(analyzer._check_s())

    def test_s_class(self):
        analyzer = self._analyze("!a", ['a'])
        self.assertTrue(analyzer.results[Constants.CLASS_S])
        analyzer = self._analyze("a&b", ['a','b'])
        self.assertFalse(analyzer.results[Constants.CLASS_S])
        analyzer = self._analyze("1", [])
        self.assertFalse(analyzer.results[Constants.CLASS_S])

    def test_m_class(self):
        analyzer = self._analyze("a&b", ['a','b'])
        self.assertTrue(analyzer.results[Constants.CLASS_M])
        analyzer = self._analyze("!a", ['a'])
        self.assertFalse(analyzer.results[Constants.CLASS_M])
        analyzer = self._analyze("a|b", ['a','b'])
        self.assertTrue(analyzer.results[Constants.CLASS_M])

    def test_l_class(self):
        analyzer = self._analyze("a~b", ['a','b'])
        self.assertTrue(analyzer.results[Constants.CLASS_L])
        analyzer = self._analyze("a&b", ['a','b'])
        self.assertFalse(analyzer.results[Constants.CLASS_L])
        analyzer = self._analyze("1", [])
        self.assertTrue(analyzer.results[Constants.CLASS_L])

    def test_print_results(self):
        analyzer = self._analyze("a&b", ['a','b'])
        analyzer.print_results()


if __name__ == '__main__':
    unittest.main()
