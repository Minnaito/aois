from constants import *

def char_value(ch: str) -> int:
    """Возвращает числовой код русской буквы."""
    return RUS_ALPHABET.get(ch.lower(), MINUS_ONE)

def compute_v(key: str) -> int:
    """Перевод ключа в числовое значение V по первым двум буквам."""
    key = key.lower()
    if len(key) < MIN_KEY_LENGTH:
        raise ValueError(f"Ключ должен содержать минимум {MIN_KEY_LENGTH} символа")
    v1 = char_value(key[ZERO])
    v2 = char_value(key[ONE])
    if v1 == MINUS_ONE or v2 == MINUS_ONE:
        raise ValueError(f"Недопустимые символы в ключе: '{key}'")
    return v1 * ALPHABET_SIZE + v2

def compute_h(key: str, table_size: int, initial_address: int) -> int:
    """Вычисление хеш-адреса h."""
    v = compute_v(key)
    return v % table_size + initial_address