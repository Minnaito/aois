import unittest
from src.KarnaughMapMinimizer import KarnaughMapMinimizer
from src.TruthTable import TruthTable
from src.ExpressionParser import BooleanExpressionParser


class TestKarnaughMapMinimizer(unittest.TestCase):
    def setUp(self):
        self.parser = BooleanExpressionParser()

    def _create_kmap(self, expr, variables):
        tt = TruthTable(variables, expr, self.parser)
        truth_table_list = [{'inputs': bits, 'output': res} for bits, res in tt]
        return KarnaughMapMinimizer(truth_table_list, variables)

    def test_one_variable_all_cases(self):
        kmap = self._create_kmap("0", ['a'])
        self.assertEqual(kmap._minimize_dnf([]), "0")
        self.assertEqual(kmap._minimize_cnf(), "0")

        kmap = self._create_kmap("1", ['a'])
        self.assertEqual(kmap._minimize_dnf([]), "1")
        self.assertEqual(kmap._minimize_cnf(), "1")

        kmap = self._create_kmap("a", ['a'])
        prime_imps = kmap._find_prime_implicants()
        self.assertEqual(kmap._minimize_dnf(prime_imps), "a")
        self.assertEqual(kmap._minimize_cnf(), "a")

        kmap = self._create_kmap("!a", ['a'])
        prime_imps = kmap._find_prime_implicants()
        self.assertEqual(kmap._minimize_dnf(prime_imps), "!a")
        self.assertEqual(kmap._minimize_cnf(), "!a")

    def test_two_variables_and(self):
        kmap = self._create_kmap("a&b", ['a','b'])
        prime_imps = kmap._find_prime_implicants()
        self.assertEqual(len(prime_imps), 1)
        # Терм теперь без ∧ - слитно "ab"
        self.assertEqual(prime_imps[0]['term'], "ab")
        minimized = kmap._minimize_dnf(prime_imps)
        self.assertEqual(minimized, "ab")

    def test_two_variables_or(self):
        kmap = self._create_kmap("a|b", ['a','b'])
        prime_imps = kmap._find_prime_implicants()
        terms = [imp['term'] for imp in prime_imps]
        self.assertIn('a', terms)
        self.assertIn('b', terms)
        minimized = kmap._minimize_dnf(prime_imps)
        self.assertIn(minimized, ["a ∨ b", "b ∨ a"])

    def test_three_variables(self):
        kmap = self._create_kmap("a&b&c", ['a','b','c'])
        self.assertEqual(kmap.n, 3)
        prime_imps = kmap._find_prime_implicants()
        result = kmap._minimize_dnf(prime_imps)
        # Терм теперь без ∧ - слитно "abc"
        self.assertEqual(result, "abc")

    def test_four_variables(self):
        kmap = self._create_kmap("a&b&c&d", ['a','b','c','d'])
        self.assertEqual(kmap.n, 4)
        prime_imps = kmap._find_prime_implicants()
        result = kmap._minimize_dnf(prime_imps)
        # Терм теперь без ∧ - слитно "abcd"
        self.assertEqual(result, "abcd")

    def test_five_variables(self):
        kmap = self._create_kmap("a&b&c&d&e", ['a','b','c','d','e'])
        self.assertEqual(kmap.n, 5)
        self.assertIsNotNone(kmap.map)

    def test_cnf_minimization(self):
        kmap = self._create_kmap("a&b", ['a', 'b'])
        cnf = kmap._minimize_cnf()
        # Для a&b КНФ будет (a) ∧ (b) - содержит ∧, а не ∨
        self.assertTrue("∧" in cnf or "&" in cnf or cnf in ["a ∧ b", "b ∧ a", "(a) ∧ (b)", "(b) ∧ (a)"])

    def test_print_kmap_one_var(self):
        kmap = self._create_kmap("a", ['a'])
        # Проверяем, что карта построена корректно
        self.assertEqual(kmap.n, 1)
        self.assertEqual(kmap.map, [0, 1])
        # Вызываем print_kmap без ошибок
        try:
            kmap.print_kmap()
        except Exception as e:
            self.fail(f"print_kmap raised exception: {e}")

    def test_cells_to_term(self):
        kmap = self._create_kmap("a&b", ['a','b'])
        # Для a&b карта: [0,0,0,1] -> клетка (1,1) даёт 1
        cells = {(1, 1)}
        term = kmap._cells_to_term(cells)
        self.assertEqual(term, "ab")

    def test_gray_to_bin(self):
        kmap = self._create_kmap("a", ['a'])
        self.assertEqual(kmap._gray_to_bin(0, 2), 0)
        self.assertEqual(kmap._gray_to_bin(1, 2), 1)
        self.assertEqual(kmap._gray_to_bin(3, 2), 2)

    def test_simplify_dnf_terms(self):
        kmap = self._create_kmap("a|b", ['a','b'])
        terms = ["a", "ab"]
        simplified = kmap._simplify_dnf_terms(terms)
        self.assertEqual(simplified, ["a"])

    def test_print_kmap_five_vars(self):
        """Тест печати карты Карно для 5 переменных"""
        kmap = self._create_kmap("a&b&c&d&e", ['a', 'b', 'c', 'd', 'e'])
        try:
            kmap.print_kmap()
        except Exception as e:
            self.fail(f"print_kmap raised exception: {e}")

    def test_build_kmap_invalid_n(self):
        """Тест построения карты с недопустимым количеством переменных"""
        with self.assertRaises(ValueError):
            kmap = KarnaughMapMinimizer([], ['a', 'b', 'c', 'd', 'e', 'f'])

    def test_get_dimensions_one_var(self):
        kmap = self._create_kmap("a", ['a'])
        rows, cols, layers = kmap._get_dimensions()
        self.assertEqual(rows, 2)
        self.assertEqual(cols, 1)
        self.assertEqual(layers, 1)

    def test_get_dimensions_two_vars(self):
        kmap = self._create_kmap("a&b", ['a','b'])
        rows, cols, layers = kmap._get_dimensions()
        self.assertEqual(rows, 2)
        self.assertEqual(cols, 2)
        self.assertEqual(layers, 1)

    def test_get_dimensions_three_vars(self):
        kmap = self._create_kmap("a&b&c", ['a','b','c'])
        rows, cols, layers = kmap._get_dimensions()
        self.assertEqual(rows, 2)
        self.assertEqual(cols, 4)
        self.assertEqual(layers, 1)

    def test_get_dimensions_four_vars(self):
        kmap = self._create_kmap("a&b&c&d", ['a','b','c','d'])
        rows, cols, layers = kmap._get_dimensions()
        self.assertEqual(rows, 4)
        self.assertEqual(cols, 4)
        self.assertEqual(layers, 1)

    def test_get_dimensions_five_vars(self):
        kmap = self._create_kmap("a&b&c&d&e", ['a','b','c','d','e'])
        rows, cols, layers = kmap._get_dimensions()
        self.assertEqual(rows, 4)
        self.assertEqual(cols, 4)
        self.assertEqual(layers, 2)

    def test_cell_to_input_vector_one_var(self):
        kmap = self._create_kmap("a", ['a'])
        vec = kmap._cell_to_input_vector((0,))
        self.assertEqual(vec, [0])
        vec = kmap._cell_to_input_vector((1,))
        self.assertEqual(vec, [1])

    def test_cell_to_input_vector_two_vars(self):
        kmap = self._create_kmap("a&b", ['a','b'])
        vec = kmap._cell_to_input_vector((0, 0))
        self.assertEqual(vec, [0, 0])
        vec = kmap._cell_to_input_vector((1, 1))
        self.assertEqual(vec, [1, 1])

    def test_cell_to_input_vector_three_vars(self):
        kmap = self._create_kmap("a&b&c", ['a','b','c'])
        vec = kmap._cell_to_input_vector((0, 0))
        self.assertEqual(vec[0], 0)
        self.assertEqual(len(vec), 3)

    def test_cell_to_input_vector_four_vars(self):
        kmap = self._create_kmap("a&b&c&d", ['a','b','c','d'])
        vec = kmap._cell_to_input_vector((0, 0))
        self.assertEqual(len(vec), 4)

    def test_cell_to_input_vector_five_vars(self):
        kmap = self._create_kmap("a&b&c&d&e", ['a','b','c','d','e'])
        vec = kmap._cell_to_input_vector((0, 0, 0))
        self.assertEqual(len(vec), 5)

    def test_find_prime_implicants_two_vars(self):
        kmap = self._create_kmap("a|b", ['a','b'])
        prime_imps = kmap._find_prime_implicants()
        self.assertGreater(len(prime_imps), 0)

    def test_find_prime_implicants_three_vars_complex(self):
        kmap = self._create_kmap("a&b|c", ['a','b','c'])
        prime_imps = kmap._find_prime_implicants()
        self.assertGreater(len(prime_imps), 0)

    def test_find_prime_implicants_four_vars_complex(self):
        kmap = self._create_kmap("a&b|c&d", ['a','b','c','d'])
        prime_imps = kmap._find_prime_implicants()
        self.assertGreater(len(prime_imps), 0)

    def test_find_prime_implicants_five_vars_complex(self):
        kmap = self._create_kmap("a&b&c|d&e", ['a','b','c','d','e'])
        prime_imps = kmap._find_prime_implicants()
        self.assertGreater(len(prime_imps), 0)

    def test_minimize_dnf_complex_two_vars(self):
        kmap = self._create_kmap("a~b", ['a','b'])
        prime_imps = kmap._find_prime_implicants()
        result = kmap._minimize_dnf(prime_imps)
        self.assertIsNotNone(result)

    def test_minimize_dnf_complex_three_vars(self):
        kmap = self._create_kmap("a&b|!a&c", ['a','b','c'])
        prime_imps = kmap._find_prime_implicants()
        result = kmap._minimize_dnf(prime_imps)
        self.assertIsNotNone(result)

    def test_minimize_cnf_complex_two_vars(self):
        kmap = self._create_kmap("a~b", ['a','b'])
        result = kmap._minimize_cnf()
        self.assertIsNotNone(result)

    def test_minimize_cnf_complex_three_vars(self):
        kmap = self._create_kmap("a&b|!a&c", ['a','b','c'])
        result = kmap._minimize_cnf()
        self.assertIsNotNone(result)

    def test_minimize_cnf_complex_four_vars(self):
        kmap = self._create_kmap("a&b&c|!a&d", ['a','b','c','d'])
        result = kmap._minimize_cnf()
        self.assertIsNotNone(result)

    def test_get_output_from_dict(self):
        kmap = self._create_kmap("a", ['a'])
        result = kmap._get_output({'output': 1})
        self.assertEqual(result, 1)
        result = kmap._get_output({'output': 0})
        self.assertEqual(result, 0)
        result = kmap._get_output({})
        self.assertEqual(result, 0)

    def test_get_output_from_int(self):
        kmap = self._create_kmap("a", ['a'])
        result = kmap._get_output(1)
        self.assertEqual(result, 1)
        result = kmap._get_output(0)
        self.assertEqual(result, 0)

    def test_cells_to_term_empty(self):
        kmap = self._create_kmap("a", ['a'])
        term = kmap._cells_to_term(set())
        self.assertEqual(term, "0")

    def test_cells_to_term_one(self):
        kmap = self._create_kmap("1", ['a','b'])
        cells = {(0,0), (0,1), (1,0), (1,1)}
        term = kmap._cells_to_term(cells)
        self.assertEqual(term, "1")

    def test_minimize_dnf_no_ones(self):
        kmap = self._create_kmap("0", ['a','b'])
        result = kmap._minimize_dnf([])
        self.assertEqual(result, "0")

    def test_minimize_cnf_no_zeros(self):
        kmap = self._create_kmap("1", ['a','b'])
        result = kmap._minimize_cnf()
        self.assertEqual(result, "1")

if __name__ == '__main__':
    unittest.main()
