# Общие целочисленные константы
ZERO = 0
ONE = 1
TWO = 2
MINUS_ONE = -1

# Параметры хеш-таблицы
TABLE_SIZE = 20
INITIAL_ADDRESS = ZERO
MAX_PROBING_ATTEMPTS = TABLE_SIZE
MAX_DATA_LENGTH = 30

# Хеш-функция и алфавит
ALPHABET_SIZE = 33
RUS_ALPHABET: dict[str, int] = {
    'а': ZERO,  'б': ONE,   'в': 2,   'г': 3,   'д': 4,   'е': 5,   'ё': 6,
    'ж': 7,    'з': 8,    'и': 9,   'й': 10,  'к': 11,  'л': 12,  'м': 13,
    'н': 14,   'о': 15,   'п': 16,  'р': 17,  'с': 18,  'т': 19,  'у': 20,
    'ф': 21,   'х': 22,   'ц': 23,  'ч': 24,  'ш': 25,  'щ': 26,  'ъ': 27,
    'ы': 28,   'ь': 29,   'э': 30,  'ю': 31,  'я': 32
}
MIN_KEY_LENGTH = TWO

# Параметры отображения
DISPLAY_LINE_LENGTH = 140
COL_WIDTH_KEY = 15
COL_WIDTH_V = 6
COL_WIDTH_H = 6
COL_WIDTH_IDX = 4
COL_WIDTH_ID = 12
COL_WIDTH_C = 4
COL_WIDTH_U = 4
COL_WIDTH_T = 4
COL_WIDTH_L = 4
COL_WIDTH_D = 4
COL_WIDTH_PO = 6
MAX_DATA_DISPLAY = 50

__all__ = [
    "ZERO", "ONE", "TWO", "MINUS_ONE",
    "TABLE_SIZE", "INITIAL_ADDRESS", "MAX_PROBING_ATTEMPTS", "MAX_DATA_LENGTH",
    "ALPHABET_SIZE", "RUS_ALPHABET", "MIN_KEY_LENGTH",
    "DISPLAY_LINE_LENGTH",
    "COL_WIDTH_KEY", "COL_WIDTH_V", "COL_WIDTH_H", "COL_WIDTH_IDX",
    "COL_WIDTH_ID", "COL_WIDTH_C", "COL_WIDTH_U", "COL_WIDTH_T",
    "COL_WIDTH_L", "COL_WIDTH_D", "COL_WIDTH_PO",
    "MAX_DATA_DISPLAY"
]