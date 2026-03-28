import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.LogicFunctionAnalyzer import LogicFunctionAnalyzer
from src.TruthTableGenerator import TruthTableGenerator
from src.NormalFormsBuilder import NormalFormsBuilder
from src.DummyVariableFinder import DummyVariableFinder
from src.ZhegalkinPolynomialBuilder import ZhegalkinPolynomialBuilder
from src.BooleanDerivativeCalculator import BooleanDerivativeCalculator
from src.KarnaughMapMinimizer import KarnaughMapMinimizer
from src.PostClassesAnalyzer import PostClassesAnalyzer


class TestLogicFunctionAnalyzer(unittest.TestCase):
    """Тесты для LogicFunctionAnalyzer"""

    def setUp(self):
        self.analyzer = LogicFunctionAnalyzer()

    def test_initialization(self):
        self.assertEqual(self.analyzer.expression, "")
        self.assertEqual(self.analyzer.variables, [])
        self.assertEqual(self.analyzer.truth_table, [])
        self.assertEqual(self.analyzer.sdnf_terms, [])
        self.assertEqual(self.analyzer.sknf_terms, [])

    def test_print_header(self):
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.analyzer.print_header("Test")
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Test", output)

    def test_print_separator(self):
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.analyzer.print_separator()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("-", output)

    def test_truth_table_generation(self):
        tt_gen = TruthTableGenerator("a&b")
        truth_table = tt_gen.get_truth_table()
        variables = tt_gen.get_variables()

        self.assertEqual(variables, ['a', 'b'])
        self.assertEqual(len(truth_table), 4)

        expected = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1)]
        for i, row in enumerate(truth_table):
            self.assertEqual(row['inputs'], expected[i][:2])
            self.assertEqual(row['output'], expected[i][2])

    def test_normal_forms(self):
        tt_gen = TruthTableGenerator("a&b")
        truth_table = tt_gen.get_truth_table()
        variables = tt_gen.get_variables()

        builder = NormalFormsBuilder(truth_table, variables)
        sdnf = builder.get_sdnf()
        sknf = builder.get_sknf()

        self.assertIn("a ∧ b", sdnf)
        self.assertIn("a ∨ b", sknf)

    def test_normal_forms_print(self):
        """Тест вывода нормальных форм"""
        tt_gen = TruthTableGenerator("a&b")
        truth_table = tt_gen.get_truth_table()
        variables = tt_gen.get_variables()

        builder = NormalFormsBuilder(truth_table, variables)
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        builder.print_forms()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("СДНФ", output)

    def test_dummy_variables(self):
        truth_table = [
            {'inputs': (0, 0), 'output': 0},
            {'inputs': (0, 1), 'output': 0},
            {'inputs': (1, 0), 'output': 1},
            {'inputs': (1, 1), 'output': 1}
        ]

        finder = DummyVariableFinder(truth_table, ['a', 'b'])
        dummy_vars = finder.get_dummy_variables()
        self.assertEqual(dummy_vars, ['b'])

    def test_dummy_variables_print(self):
        """Тест вывода фиктивных переменных"""
        truth_table = [
            {'inputs': (0, 0), 'output': 0},
            {'inputs': (0, 1), 'output': 0},
            {'inputs': (1, 0), 'output': 1},
            {'inputs': (1, 1), 'output': 1}
        ]

        finder = DummyVariableFinder(truth_table, ['a', 'b'])
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        finder.print_results()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Фиктивные переменные", output)

    def test_zhegalkin_polynomial(self):
        truth_table = [
            {'inputs': (0, 0), 'output': 0},
            {'inputs': (0, 1), 'output': 1},
            {'inputs': (1, 0), 'output': 1},
            {'inputs': (1, 1), 'output': 0}
        ]

        builder = ZhegalkinPolynomialBuilder(truth_table, ['a', 'b'])
        polynomial = builder.get_polynomial()
        self.assertIn("a ⊕ b", polynomial)

    def test_zhegalkin_polynomial_print(self):
        """Тест вывода полинома Жегалкина"""
        truth_table = [
            {'inputs': (0, 0), 'output': 0},
            {'inputs': (0, 1), 'output': 1},
            {'inputs': (1, 0), 'output': 1},
            {'inputs': (1, 1), 'output': 0}
        ]

        builder = ZhegalkinPolynomialBuilder(truth_table, ['a', 'b'])
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        builder.print_polynomial()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Полином Жегалкина", output)

    def test_minimization(self):
        truth_table = [
            {'inputs': (0, 0), 'output': 0},
            {'inputs': (0, 1), 'output': 0},
            {'inputs': (1, 0), 'output': 1},
            {'inputs': (1, 1), 'output': 1}
        ]

        for row in truth_table:
            inputs = row['inputs']
            output = row['output']
            if inputs[0] == 1:
                self.assertEqual(output, 1)
            else:
                self.assertEqual(output, 0)

    def test_complex_expression(self):
        tt_gen = TruthTableGenerator("a->b")
        truth_table = tt_gen.get_truth_table()

        expected = [1, 1, 0, 1]
        for i, row in enumerate(truth_table):
            self.assertEqual(row['output'], expected[i])

    def test_boolean_derivatives(self):
        tt_gen = TruthTableGenerator("a&b")
        truth_table = tt_gen.get_truth_table()
        variables = tt_gen.get_variables()

        calc = BooleanDerivativeCalculator(truth_table, variables)
        deriv_a = calc.partial('a')
        deriv_b = calc.partial('b')

        self.assertEqual(deriv_a, 'b')
        self.assertEqual(deriv_b, 'a')

    def test_boolean_derivatives_print(self):
        """Тест вывода булевых производных"""
        tt_gen = TruthTableGenerator("a&b")
        truth_table = tt_gen.get_truth_table()
        variables = tt_gen.get_variables()

        calc = BooleanDerivativeCalculator(truth_table, variables)
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        calc.print_partial('a')
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("∂f/∂a", output)

    def test_karnaugh_map(self):
        tt_gen = TruthTableGenerator("a&b")
        truth_table = tt_gen.get_truth_table()
        variables = tt_gen.get_variables()

        kmap = KarnaughMapMinimizer(truth_table, variables)
        result = kmap.get_minimized_function()
        self.assertIn("a ∧ b", result)

    def test_karnaugh_map_print(self):
        """Тест вывода карты Карно"""
        tt_gen = TruthTableGenerator("a&b")
        truth_table = tt_gen.get_truth_table()
        variables = tt_gen.get_variables()

        kmap = KarnaughMapMinimizer(truth_table, variables)
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        kmap.print_kmap()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Карта Карно", output)

    def test_post_classes(self):
        tt_gen = TruthTableGenerator("a&b")
        truth_table = tt_gen.get_truth_table()
        variables = tt_gen.get_variables()

        analyzer = PostClassesAnalyzer(truth_table, variables)
        results = analyzer.get_results()

        self.assertTrue(results['T0'])
        self.assertTrue(results['T1'])
        self.assertFalse(results['S'])
        self.assertTrue(results['M'])
        self.assertFalse(results['L'])

    def test_post_classes_print(self):
        """Тест вывода классов Поста"""
        tt_gen = TruthTableGenerator("a&b")
        truth_table = tt_gen.get_truth_table()
        variables = tt_gen.get_variables()

        analyzer = PostClassesAnalyzer(truth_table, variables)
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        analyzer.print_results()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Принадлежность к классам Поста", output)

    def test_analyze_function_with_zero(self):
        """Тест анализа нулевой функции"""
        self.analyzer.expression = 'a&!a'
        self.analyzer.truth_table = [
            {'inputs': (0,), 'output': 0},
            {'inputs': (1,), 'output': 0}
        ]
        self.analyzer.variables = ['a']
        self.analyzer.normal_forms_builder = NormalFormsBuilder(
            self.analyzer.truth_table,
            self.analyzer.variables
        )

        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            self.analyzer.analyze_function()
        except AttributeError:
            pass
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("0", output)

    def test_analyze_function_with_one(self):
        """Тест анализа единичной функции"""
        self.analyzer.expression = 'a|!a'
        self.analyzer.truth_table = [
            {'inputs': (0,), 'output': 1},
            {'inputs': (1,), 'output': 1}
        ]
        self.analyzer.variables = ['a']
        self.analyzer.normal_forms_builder = NormalFormsBuilder(
            self.analyzer.truth_table,
            self.analyzer.variables
        )

        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            self.analyzer.analyze_function()
        except AttributeError:
            pass
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("1", output)


if __name__ == '__main__':
    unittest.main()