from src.BooleanFunction import BooleanFunction

class FullAdderSKNF:
    def __init__(self):
        self.input_names = ['A', 'B', 'Cin']
        sum_tt = [0, 1, 1, 0, 1, 0, 0, 1]
        cout_tt = [0, 0, 0, 1, 0, 1, 1, 1]
        self.sum_func = BooleanFunction(sum_tt, self.input_names)
        self.cout_func = BooleanFunction(cout_tt, self.input_names)

    def get_sknf(self):
        """Возвращает словарь с СКНФ для Sum и Cout."""
        return {
            'Sum': self.sum_func.to_sknf(),
            'Cout': self.cout_func.to_sknf()
        }

    def display(self):
        """Выводит информацию о сумматоре и его СКНФ."""
        sknf = self.get_sknf()
        print("Одноразрядный двоичный сумматор на 3 входа (ОДС-3)")
        print("Представление выходных функций в СКНФ:")
        print(f"Sum = {sknf['Sum']}")
        print(f"Cout = {sknf['Cout']}")