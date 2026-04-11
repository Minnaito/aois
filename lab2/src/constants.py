class Constants:
    # Числовые константы
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

    # Индексы
    ZERO_INDEX = 0
    FIRST_INDEX = 1
    SECOND_INDEX = 2
    THIRD_INDEX = 3
    FOURTH_INDEX = 4
    ZERO_GROUP = 0
    FIRST_GROUP = 1
    SECOND_GROUP = 2

    # Операционные системы
    OS_WINDOWS = 'nt'
    CLEAR_CMD_WINDOWS = 'cls'
    CLEAR_CMD_UNIX = 'clear'

    # Коды выхода
    EXIT_SUCCESS = 0

    # Максимальное количество переменных
    MAX_VARIABLES = 5

    # Доступные переменные
    VARIABLES = ['a', 'b', 'c', 'd', 'e']

    # Классы Поста
    CLASS_T0 = "T0"
    CLASS_T1 = "T1"
    CLASS_S = "S"
    CLASS_M = "M"
    CLASS_L = "L"

    # Типы производных
    DERIVATIVE_SIMPLE = "simple"
    DERIVATIVE_MIXED = "mixed"

    # Размеры для карт Карно
    KMAP_ORDER_2 = ['00', '01', '11', '10']
    KMAP_ORDER_3 = ['00', '01', '11', '10']
    KMAP_ORDER_4 = ['00', '01', '11', '10']

    # Размеры прямоугольников для карт Карно
    KMAP_RECT_SIZES_2 = [(2, 2), (2, 1), (1, 2), (1, 1)]
    KMAP_RECT_SIZES_3 = [(4, 2), (2, 4), (4, 1), (1, 4), (2, 2), (2, 1), (1, 2), (1, 1)]
    KMAP_RECT_SIZES_4 = [(4, 4), (4, 2), (2, 4), (4, 1), (1, 4), (2, 2), (2, 1), (1, 2), (1, 1)]
    KMAP_RECT_SIZES_5 = [(2, 2), (2, 1), (1, 2), (1, 1)]


    BINARY_FORMAT_SPEC = 'b'
    GLUE_DIFF_COUNT = 1
    MAX_GLUE_ITERATIONS = 20
    SINGLE_COVER = 1
    TABLE_COVER_MARK = 'X'
    VARIABLE_PATTERN = r'[a-zA-Z][a-zA-Z0-9]*'
    KEYWORDS = {'not', 'and', 'or', 'xor', 'True', 'False', 'None'}
    BUILTINS_KEY = '__builtins__'
    PAREN_OPEN = '('
    PAREN_CLOSE = ')'
    INPUTS_KEY = 'inputs'
    OUTPUT_KEY = 'output'
    OUTPUT_LABEL = 'F'

    # Примеры функций
    EXAMPLE_1 = "!(!a->!b)|c"
    EXAMPLE_2 = "a&b|c"
    EXAMPLE_3 = "a->b"
    EXAMPLE_4 = "a~b"

    # Минимальное количество переменных
    MIN_VARS_FOR_PARTIAL = 1
    MIN_VARS_FOR_MIXED = 2

    # Символы форматирования
    SEPARATOR = "-" * 70
    LINE = "=" * 70
    TABLE_WIDTH = 80
    MIN_IMP_COL_WIDTH = 20
    TABLE_COLUMN_SPACING = 8

    # Бинарные значения
    BINARY_ZERO = '0'
    BINARY_ONE = '1'
    BINARY_X = 'X'

    # Символы операций
    OP_NOT = '!'
    OP_AND = '&'
    OP_OR = '|'
    OP_XOR = '^'
    OP_IMPL = '->'
    OP_EQUIV = '~'
    OP_OR_SYMBOL = '∨'
    OP_AND_SYMBOL = '∧'

    # Строковые представления операций
    OP_NOT_STR = 'not'
    OP_AND_STR = 'and'
    OP_OR_STR = 'or'
    OP_XOR_STR = '!='
    OP_EQUIV_STR = '=='
    OP_IMPL_PATTERN = r'([^()\s]+)\s*->\s*([^()\s]+)'

    # Значения по умолчанию
    DEFAULT_OUTPUT_ZERO = "0"
    DEFAULT_OUTPUT_ONE = "1"

    # Индексы для таблицы
    TABLE_HEADER_SEP = " | "
    TABLE_ROW_SEP = " | "

    # Множители для размеров
    POWER_BASE = 2

    @classmethod
    def get_variables_up_to(cls, n):
        """Получить список переменных до указанного индекса"""
        return cls.VARIABLES[:n]

    @classmethod
    def get_kmap_order(cls, n):
        """Получить порядок для карты Карно в зависимости от количества переменных"""
        if n == cls.TWO or n == cls.THREE or n == cls.FOUR:
            return cls.KMAP_ORDER_2
        return cls.KMAP_ORDER_4

    @classmethod
    def get_rect_sizes(cls, n):
        """Получить размеры прямоугольников для карты Карно"""
        if n == cls.TWO:
            return cls.KMAP_RECT_SIZES_2
        elif n == cls.THREE:
            return cls.KMAP_RECT_SIZES_3
        elif n == cls.FOUR:
            return cls.KMAP_RECT_SIZES_4
        else:
            return cls.KMAP_RECT_SIZES_5

    @classmethod
    def format_error(cls, error_template, **kwargs):
        """Форматирование сообщения об ошибке (больше не используется, оставлено для совместимости)"""
        return error_template.format(**kwargs)
