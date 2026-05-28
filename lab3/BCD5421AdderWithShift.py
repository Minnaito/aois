class BCD5421AdderWithShift:
    def __init__(self, shift=4):
        self.shift = shift
        self.digit_to_5421 = {
            0: (0,0,0,0), 1: (0,0,0,1), 2: (0,0,1,0), 3: (0,0,1,1),
            4: (0,1,0,0), 5: (0,1,0,1), 6: (0,1,1,0), 7: (0,1,1,1),
            8: (1,0,0,0), 9: (1,0,0,1)
        }
        self.reverse_5421 = {v: k for k, v in self.digit_to_5421.items()}

    def add(self, a_5421, b_5421):
        a_digit = self.reverse_5421.get(a_5421, None)
        b_digit = self.reverse_5421.get(b_5421, None)
        if a_digit is None or b_digit is None:
            raise ValueError("Неверный код 5421")
        total = a_digit + b_digit + self.shift
        overflow = total >= 20
        units = total % 10
        tens = (total // 10) % 10
        if total >= 20:
            tens = 0
        units_5421 = self.digit_to_5421[units]
        tens_5421 = self.digit_to_5421[tens]
        return units_5421, tens_5421, overflow

    def generate_truth_table(self):
        inputs = []
        outputs = []
        for a in range(10):
            for b in range(10):
                a_code = self.digit_to_5421[a]
                b_code = self.digit_to_5421[b]
                units, tens, ovf = self.add(a_code, b_code)
                inputs.append(list(a_code) + list(b_code))
                outputs.append(list(units) + list(tens) + [ovf])
        return inputs, outputs

    def synthesize(self):
        print("Синтез комбинационной схемы для сложения двух чисел в коде 5421 со смещением 4.")
        print("Рекомендуется построить схему на основе 8-разрядного двоичного сумматора,")
        print("добавить константу 4 и выполнить коррекцию результата в код 5421.")
        print("В Logisim можно использовать готовые сумматоры и логические вентили.")
        print("\nПримеры работы:")
        inputs, outputs = self.generate_truth_table()
        for i in range(0, 100, 20):
            a = i // 10
            b = i % 10
            units, tens, ovf = self.add(self.digit_to_5421[a], self.digit_to_5421[b])
            print(f"{a} + {b} + 4 = {tens*10+units} (единицы: {units}, десятки: {tens}, переполнение: {ovf})")