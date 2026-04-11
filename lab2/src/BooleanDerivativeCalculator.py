import re
from itertools import combinations, product
from typing import List, Dict, Tuple, Union

from src.constants import Constants


class BooleanDerivativeCalculator:
    def __init__(self, expression: Union[str, List], variables: List[str]):
        if isinstance(expression, str):
            self.expression = expression
        else:
            self.expression = ""
        self.variables = sorted(variables)
        self.var_to_index = {var: idx for idx, var in enumerate(self.variables)}
        if isinstance(expression, list) and len(expression) > Constants.ZERO and isinstance(expression[Constants.ZERO_INDEX], dict):
            self.truth_table = self._convert_table_to_dict(expression)
        else:
            self.truth_table = self._build_truth_table()

    def _convert_table_to_dict(self, table: List[dict]) -> Dict[Tuple[int, ...], int]:
        truth_table = {}
        for row in table:
            inputs = row['inputs']
            truth_table[inputs] = row['output']
        return truth_table

    def _evaluate(self, expr: str, values: Dict[str, int]) -> int:
        if not expr:
            return Constants.ZERO
        local_expr = expr
        for var, val in values.items():
            local_expr = local_expr.replace(var, str(val))
        while Constants.OP_IMPL in local_expr:
            match = re.search(Constants.OP_IMPL_PATTERN, local_expr)
            if match:
                left, right = match.group(Constants.FIRST_INDEX), match.group(Constants.SECOND_INDEX)
                local_expr = local_expr.replace(match.group(Constants.ZERO_INDEX), f'(~{left}|{right})')
            else:
                break
        local_expr = local_expr.replace(Constants.OP_NOT, f' {Constants.OP_NOT_STR} ')
        local_expr = local_expr.replace(Constants.OP_AND, f' {Constants.OP_AND_STR} ')
        local_expr = local_expr.replace(Constants.OP_OR, f' {Constants.OP_OR_STR} ')
        local_expr = local_expr.replace(Constants.OP_XOR, f' {Constants.OP_XOR_STR} ')
        local_expr = local_expr.replace(Constants.OP_EQUIV, f' {Constants.OP_EQUIV_STR} ')
        local_expr = local_expr.replace('(', ' ( ')
        local_expr = local_expr.replace(')', ' ) ')
        try:
            def xor(x, y):
                return (x and not y) or (not x and y)
            result = eval(local_expr, {'__builtins__': None}, {'xor': xor})
            return Constants.ONE if result else Constants.ZERO
        except:
            return self._evaluate_simple(local_expr)

    def _evaluate_simple(self, expr: str) -> int:
        expr = expr.strip()
        if expr.startswith('(') and expr.endswith(')'):
            return self._evaluate_simple(expr[Constants.FIRST_INDEX:-Constants.FIRST_INDEX])
        if expr.startswith(f'{Constants.OP_NOT_STR} '):
            return Constants.ONE - self._evaluate_simple(expr[Constants.FOUR:])
        if f' {Constants.OP_AND_STR} ' in expr:
            parts = expr.split(f' {Constants.OP_AND_STR} ', Constants.FIRST_INDEX)
            return self._evaluate_simple(parts[Constants.ZERO_INDEX]) and self._evaluate_simple(parts[Constants.FIRST_INDEX])
        if f' {Constants.OP_OR_STR} ' in expr:
            parts = expr.split(f' {Constants.OP_OR_STR} ', Constants.FIRST_INDEX)
            return self._evaluate_simple(parts[Constants.ZERO_INDEX]) or self._evaluate_simple(parts[Constants.FIRST_INDEX])
        if f' {Constants.OP_XOR_STR} ' in expr:
            parts = expr.split(f' {Constants.OP_XOR_STR} ', Constants.FIRST_INDEX)
            left = self._evaluate_simple(parts[Constants.ZERO_INDEX])
            right = self._evaluate_simple(parts[Constants.FIRST_INDEX])
            return (left and not right) or (not left and right)
        if f' {Constants.OP_EQUIV_STR} ' in expr:
            parts = expr.split(f' {Constants.OP_EQUIV_STR} ', Constants.FIRST_INDEX)
            return Constants.ONE if self._evaluate_simple(parts[Constants.ZERO_INDEX]) == self._evaluate_simple(parts[Constants.FIRST_INDEX]) else Constants.ZERO
        try:
            return int(expr)
        except:
            return Constants.ZERO

    def _build_truth_table(self) -> Dict[Tuple[int, ...], int]:
        truth_table = {}
        n = len(self.variables)
        for bits in product([Constants.ZERO, Constants.ONE], repeat=n):
            values = dict(zip(self.variables, bits))
            truth_table[bits] = self._evaluate(self.expression, values)
        return truth_table

    def _get_value(self, values: Dict[str, int]) -> int:
        key = tuple(values.get(v, Constants.ZERO) for v in self.variables)
        return self.truth_table.get(key, Constants.ZERO)

    def partial(self, var: str) -> str:
        """Частная производная по одной переменной"""
        if var not in self.var_to_index:
            raise ValueError(f"Variable {var} not found")
        other_vars = [v for v in self.variables if v != var]
        values = []
        for bits in product([Constants.ZERO, Constants.ONE], repeat=len(other_vars)):
            fixed = dict(zip(other_vars, bits))
            val0 = self._get_value({**fixed, var: Constants.ZERO})
            val1 = self._get_value({**fixed, var: Constants.ONE})
            values.append(val0 ^ val1)
        expr = self._to_expression(values, other_vars)
        return self._simplify(expr, other_vars)

    def mixed(self, vars_list: List[str]) -> str:
        """Смешанная производная по списку переменных (1–4)"""
        for v in vars_list:
            if v not in self.var_to_index:
                raise ValueError(f"Variable {v} not found")
        if len(set(vars_list)) != len(vars_list):
            raise ValueError("Duplicate variables")
        if len(vars_list) == Constants.ONE:
            return self.partial(vars_list[Constants.ZERO_INDEX])
        other_vars = [v for v in self.variables if v not in vars_list]
        k = len(vars_list)
        values = []
        for bits in product([Constants.ZERO, Constants.ONE], repeat=len(other_vars)):
            fixed = dict(zip(other_vars, bits))
            xor_sum = Constants.ZERO
            for diff_bits in product([Constants.ZERO, Constants.ONE], repeat=k):
                vals = {**fixed}
                for i, var in enumerate(vars_list):
                    vals[var] = diff_bits[i]
                xor_sum ^= self._get_value(vals)
            values.append(xor_sum)
        expr = self._to_expression(values, other_vars)
        return self._simplify(expr, other_vars)

    def print_all(self, max_order: int = Constants.FOUR):
        """Вывод всех производных до указанного порядка"""
        print(f"\n{Constants.LINE}")
        print("6. БУЛЕВЫ ПРОИЗВОДНЫЕ:")
        print(Constants.LINE)

        print("\nЧастные производные:")
        for var in self.variables:
            print(f"  ∂f/∂{var} = {self.partial(var)}")

        if max_order >= Constants.TWO and len(self.variables) >= Constants.TWO:
            print("\nСмешанные производные (по 2 переменным):")
            for var1, var2 in combinations(self.variables, Constants.TWO):
                print(f"  ∂²f/∂{var1}∂{var2} = {self.mixed([var1, var2])}")

        if max_order >= Constants.THREE and len(self.variables) >= Constants.THREE:
            print("\nСмешанные производные (по 3 переменным):")
            for combo in combinations(self.variables, Constants.THREE):
                s = "∂³f/∂" + "∂".join(combo)
                print(f"  {s} = {self.mixed(list(combo))}")

        if max_order >= Constants.FOUR and len(self.variables) >= Constants.FOUR:
            print("\nСмешанные производные (по 4 переменным):")
            for combo in combinations(self.variables, Constants.FOUR):
                s = "∂⁴f/∂" + "∂".join(combo)
                print(f"  {s} = {self.mixed(list(combo))}")

    def _to_expression(self, values: List[int], variables: List[str]) -> str:
        if not variables:
            return str(values[Constants.ZERO_INDEX])
        if all(v == Constants.ZERO for v in values):
            return Constants.DEFAULT_OUTPUT_ZERO
        if all(v == Constants.ONE for v in values):
            return Constants.DEFAULT_OUTPUT_ONE
        terms = []
        n = len(variables)
        for i, val in enumerate(values):
            if val == Constants.ONE:
                bits = [(i >> (n - Constants.ONE - j)) & Constants.ONE for j in range(n)]
                term_parts = []
                for var, bit in zip(variables, bits):
                    term_parts.append(var if bit else f"¬{var}")
                term = " ∧ ".join(term_parts) if len(term_parts) > Constants.ONE else term_parts[Constants.ZERO_INDEX]
                terms.append(term)
        return " ∨ ".join(terms)

    def _simplify(self, expr: str, variables: List[str]) -> str:
        if expr in (Constants.DEFAULT_OUTPUT_ZERO, Constants.DEFAULT_OUTPUT_ONE):
            return expr
        terms = list(set(expr.split(" ∨ ")))
        changed = True
        while changed:
            changed = False
            to_remove = set()
            for i, t1 in enumerate(terms):
                for j, t2 in enumerate(terms):
                    if i != j and self._covers(t1, t2):
                        to_remove.add(t2)
                        changed = True
            if to_remove:
                terms = [t for t in terms if t not in to_remove]
                continue
            for var in variables:
                neg = f"¬{var}"
                pos = var
                neg_terms = [t for t in terms if self._contains_literal(t, neg) and not self._contains_literal(t, pos)]
                pos_terms = [t for t in terms if self._contains_literal(t, pos) and not self._contains_literal(t, neg)]
                for t_neg in neg_terms:
                    for t_pos in pos_terms:
                        rest_neg = self._remove_literal(t_neg, neg)
                        rest_pos = self._remove_literal(t_pos, pos)
                        if rest_neg == rest_pos:
                            new = rest_neg if rest_neg else Constants.DEFAULT_OUTPUT_ONE
                            terms.remove(t_neg)
                            terms.remove(t_pos)
                            if new != Constants.DEFAULT_OUTPUT_ONE or Constants.DEFAULT_OUTPUT_ONE not in terms:
                                terms.append(new)
                            changed = True
                            break
                    if changed:
                        break
                if changed:
                    break
        result = []
        for t in terms:
            if t == Constants.DEFAULT_OUTPUT_ONE:
                return Constants.DEFAULT_OUTPUT_ONE
            if t == Constants.DEFAULT_OUTPUT_ZERO:
                continue
            if t.startswith('(') and t.endswith(')'):
                t = t[Constants.FIRST_INDEX:-Constants.FIRST_INDEX]
            result.append(t)
        if not result:
            return Constants.DEFAULT_OUTPUT_ZERO
        return " ∨ ".join(sorted(set(result)))

    def _covers(self, term1: str, term2: str) -> bool:
        lits1 = set(self._literals(term1))
        lits2 = set(self._literals(term2))
        return lits2.issubset(lits1) and lits1 != lits2

    def _literals(self, term: str) -> List[str]:
        return term.split(" ∧ ") if " ∧ " in term else [term]

    def _contains_literal(self, term: str, lit: str) -> bool:
        return lit in self._literals(term)

    def _remove_literal(self, term: str, lit: str) -> str:
        lits = [l for l in self._literals(term) if l != lit]
        if not lits:
            return ""
        if len(lits) == Constants.ONE:
            return lits[Constants.ZERO_INDEX]
        return " ∧ ".join(lits)
