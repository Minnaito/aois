import unittest
from src.LogicFunctionAnalyzer import LogicFunctionAnalyzer
from src.constants import Constants


class TestLogicFunctionAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = LogicFunctionAnalyzer()

    def test_initial_state(self):
        self.assertEqual(self.analyzer.expression, "")
        self.assertEqual(self.analyzer.variables, [])
        self.assertEqual(self.analyzer.truth_table, [])
        self.assertEqual(self.analyzer.sdnf_terms, [])
        self.assertEqual(self.analyzer.sknf_terms, [])
        self.assertIsNone(self.analyzer.normal_forms_builder)
        self.assertIsNone(self.analyzer.boolean_function)

    def test_convert_truth_table_format_empty(self):
        self.analyzer.boolean_function = None
        result = self.analyzer._convert_truth_table_format()
        self.assertEqual(result, [])

    def test_convert_truth_table_format_with_data(self):
        class MockBooleanFunction:
            def __init__(self):
                self.truth_table = [((0,), 0), ((1,), 1)]

        self.analyzer.boolean_function = MockBooleanFunction()
        result = self.analyzer._convert_truth_table_format()
        expected = [
            {'inputs': (0,), 'output': 0},
            {'inputs': (1,), 'output': 1}
        ]
        self.assertEqual(result, expected)

    def test_print_truth_table_no_bf(self):
        try:
            self.analyzer._print_truth_table()
        except Exception as e:
            self.fail(f"_print_truth_table raised: {e}")

    def test_print_truth_table_with_bf(self):
        class MockBooleanFunction:
            def __init__(self):
                self.truth_table = [((0,), 0), ((1,), 1)]

        self.analyzer.boolean_function = MockBooleanFunction()
        self.analyzer.variables = ['a']
        try:
            self.analyzer._print_truth_table()
        except Exception as e:
            self.fail(f"_print_truth_table raised: {e}")

    def test_clear_screen(self):
        try:
            self.analyzer.clear_screen()
        except Exception as e:
            self.fail(f"clear_screen raised: {e}")

    def test_print_header_and_separator(self):
        try:
            self.analyzer.print_header("TEST")
            self.analyzer.print_separator()
        except Exception as e:
            self.fail(f"print_header/print_separator raised: {e}")

    def test_analyze_function_minimal(self):
        self.analyzer.expression = "a"
        self.analyzer.variables = ['a']
        self.analyzer.truth_table = [{'inputs': (0,), 'output': 0}, {'inputs': (1,), 'output': 1}]
        self.analyzer.sdnf_terms = [1]
        self.analyzer.sknf_terms = [0]

        from src.NormalFormsBuilder import NormalFormsBuilder
        self.analyzer.normal_forms_builder = NormalFormsBuilder(self.analyzer.truth_table, self.analyzer.variables)

        try:
            self.analyzer.analyze_function()
        except Exception as e:
            self.fail(f"analyze_function raised: {e}")

    def test_run_keyboard_interrupt(self):
        # Проверяем обработку KeyboardInterrupt в main()
        import src.LogicFunctionAnalyzer as lfa
        original_run = lfa.LogicFunctionAnalyzer.run
        def mock_run(self):
            raise KeyboardInterrupt()
        lfa.LogicFunctionAnalyzer.run = mock_run
        try:
            with self.assertRaises(SystemExit) as cm:
                lfa.main()
            self.assertEqual(cm.exception.code, 0)
        finally:
            lfa.LogicFunctionAnalyzer.run = original_run

    def test_convert_truth_table_format_multiple_vars(self):
        class MockBooleanFunction:
            def __init__(self):
                self.truth_table = [((0,0), 0), ((0,1), 1), ((1,0), 1), ((1,1), 1)]

        self.analyzer.boolean_function = MockBooleanFunction()
        result = self.analyzer._convert_truth_table_format()
        expected = [
            {'inputs': (0,0), 'output': 0},
            {'inputs': (0,1), 'output': 1},
            {'inputs': (1,0), 'output': 1},
            {'inputs': (1,1), 'output': 1}
        ]
        self.assertEqual(result, expected)

    def test_print_truth_table_three_vars(self):
        class MockBooleanFunction:
            def __init__(self):
                self.truth_table = [((0,0,0), 0), ((0,0,1), 0), ((0,1,0), 0), ((0,1,1), 0),
                                   ((1,0,0), 0), ((1,0,1), 0), ((1,1,0), 0), ((1,1,1), 1)]

        self.analyzer.boolean_function = MockBooleanFunction()
        self.analyzer.variables = ['a','b','c']
        try:
            self.analyzer._print_truth_table()
        except Exception as e:
            self.fail(f"_print_truth_table raised: {e}")

    def test_analyze_function_with_two_vars(self):
        self.analyzer.expression = "a|b"
        self.analyzer.variables = ['a','b']
        self.analyzer.truth_table = [
            {'inputs': (0,0), 'output': 0},
            {'inputs': (0,1), 'output': 1},
            {'inputs': (1,0), 'output': 1},
            {'inputs': (1,1), 'output': 1}
        ]
        self.analyzer.sdnf_terms = [1,2,3]
        self.analyzer.sknf_terms = [0]

        from src.NormalFormsBuilder import NormalFormsBuilder
        self.analyzer.normal_forms_builder = NormalFormsBuilder(self.analyzer.truth_table, self.analyzer.variables)

        try:
            self.analyzer.analyze_function()
        except Exception as e:
            self.fail(f"analyze_function raised: {e}")

    def test_analyze_function_constant_zero(self):
        self.analyzer.expression = "0"
        self.analyzer.variables = ['a']
        self.analyzer.truth_table = [{'inputs': (0,), 'output': 0}, {'inputs': (1,), 'output': 0}]
        self.analyzer.sdnf_terms = []
        self.analyzer.sknf_terms = [0,1]

        from src.NormalFormsBuilder import NormalFormsBuilder
        self.analyzer.normal_forms_builder = NormalFormsBuilder(self.analyzer.truth_table, self.analyzer.variables)

        try:
            self.analyzer.analyze_function()
        except Exception as e:
            self.fail(f"analyze_function raised: {e}")

    def test_analyze_function_constant_one(self):
        self.analyzer.expression = "1"
        self.analyzer.variables = ['a']
        self.analyzer.truth_table = [{'inputs': (0,), 'output': 1}, {'inputs': (1,), 'output': 1}]
        self.analyzer.sdnf_terms = [0,1]
        self.analyzer.sknf_terms = []

        from src.NormalFormsBuilder import NormalFormsBuilder
        self.analyzer.normal_forms_builder = NormalFormsBuilder(self.analyzer.truth_table, self.analyzer.variables)

        try:
            self.analyzer.analyze_function()
        except Exception as e:
            self.fail(f"analyze_function raised: {e}")

    def test_analyze_function_five_vars(self):
        self.analyzer.expression = "a&b&c&d&e"
        self.analyzer.variables = ['a','b','c','d','e']
        truth_table = []
        for i in range(32):
            bits = tuple((i >> j) & 1 for j in range(4, -1, -1))
            truth_table.append({'inputs': bits, 'output': 1 if i == 31 else 0})
        self.analyzer.truth_table = truth_table
        self.analyzer.sdnf_terms = [31]
        self.analyzer.sknf_terms = list(range(31))

        from src.NormalFormsBuilder import NormalFormsBuilder
        self.analyzer.normal_forms_builder = NormalFormsBuilder(self.analyzer.truth_table, self.analyzer.variables)

        try:
            self.analyzer.analyze_function()
        except Exception as e:
            self.fail(f"analyze_function raised: {e}")


if __name__ == '__main__':
    unittest.main()
