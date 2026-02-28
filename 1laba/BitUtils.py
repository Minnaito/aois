class BitUtils:
    @staticmethod
    def show_bits(bits):
        """Форматирует список битов в строку с пробелами каждые 4 бита"""
        if not bits:
            return ""

        # Преобразуем каждый бит в строку и соединяем
        bits_str = ''.join(str(b) for b in bits)

        # Разбиваем на группы по 4 бита
        groups = []
        for i in range(0, len(bits_str), 4):
            groups.append(bits_str[i:i + 4])

        # Соединяем группы пробелами
        return ' '.join(groups)