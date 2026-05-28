class DownCounter8States:
    """
    Двоичный вычитающий счётчик на 8 внутренних состояний (3 бита).
    Реализован на T-триггерах. Логика управления приведена к базису НЕ-И, ИЛИ.
    """
    def __init__(self):
        self.states = list(range(8))
        self.transitions = self._build_transitions()
        self.t_excitations = self._compute_t_excitations()

    def _build_transitions(self):
        """Таблица переходов: текущее -> следующее (вычитание по модулю 8)."""
        trans = {}
        for state in range(8):
            trans[state] = (state - 1) & 7
        return trans

    def _compute_t_excitations(self):
        """Вычисляет значения T-входов для каждого триггера в каждом состоянии."""
        t = {}
        for state in range(8):
            q2 = (state >> 2) & 1
            q1 = (state >> 1) & 1
            q0 = state & 1
            nxt = self.transitions[state]
            nq2 = (nxt >> 2) & 1
            nq1 = (nxt >> 1) & 1
            nq0 = nxt & 1
            t2 = q2 ^ nq2
            t1 = q1 ^ nq1
            t0 = q0 ^ nq0
            t[state] = (t2, t1, t0)
        return t

    def minimize_expressions(self):
        t0_expr = "1"
        t1_expr = "~Q0"
        t2_expr = "~(Q1 + Q0)"
        t1_nand = "NAND(Q0, Q0)"
        t2_nand = "NAND( (Q1 OR Q0), (Q1 OR Q0) )"
        return t0_expr, t1_nand, t2_nand

    def display_schematic(self):
        """Выводит описание схемы счётчика."""
        t0, t1, t2 = self.minimize_expressions()
        print("Двоичный вычитающий счётчик на 8 состояний (3 бита)")
        print("Используются T-триггеры (тактирование по положительному фронту).")
        print("Логика управления входами T (в базисе НЕ-И, ИЛИ):")
        print(f"T0 = {t0}")
        print(f"T1 = {t1}")
        print(f"T2 = {t2}")
        print("\nСхема подключения:")
        print("- Тактовый сигнал CLK подаётся на все T-триггеры.")
        print("- T0 соединён с логической '1'.")
        print("- T1 = NAND(Q0, Q0)  (инвертор)")
        print("- T2 = NAND( (Q1 OR Q0), (Q1 OR Q0) )  (OR + инвертор)")
        print("- Выходы триггеров Q2, Q1, Q0 образуют текущее состояние (Q2 – старший бит).")