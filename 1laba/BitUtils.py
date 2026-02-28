class BitUtils:
    @staticmethod
    def show_bits(bits):
        """Форматирует список битов в строку с пробелами каждые 4 бита"""
        if not bits:
            return ""

        bits_str = ''.join(str(b) for b in bits)

        groups = []
        for i in range(0, len(bits_str), 4):
            groups.append(bits_str[i:i + 4])

        return ' '.join(groups)
