from src.FullAdderSKNF import FullAdderSKNF
from src.BCD5421AdderWithShift import BCD5421AdderWithShift
from src.DownCounter8States import DownCounter8States

def main():
    print("=== Часть 1: Одноразрядный двоичный сумматор на 3 входа (ОДС-3) ===")
    adder = FullAdderSKNF()
    adder.display()

    print("\n=== Часть 2: Сложение двух одноразрядных чисел в коде 5421 со смещением n=4 ===")
    bcd_adder = BCD5421AdderWithShift(shift=4)
    bcd_adder.synthesize()

    print("\n=== Часть 3: Двоичный вычитающий счётчик на 8 состояний ===")
    counter = DownCounter8States()
    counter.display_schematic()

if __name__ == "__main__":
    main()
