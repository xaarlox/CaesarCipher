# Alphabets: Ukr (33 letters) and Eng (26 letters)
UKR_LOWER = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
UKR_UPPER = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
ENG_LOWER = "abcdefghijklmnopqrstuvwxyz"
ENG_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def validate_key(key):
    if isinstance(key, bool):
        raise ValueError("Ключ не може бути булевим значенням")
    try:
        return int(key)
    except (TypeError, ValueError):
        raise ValueError(f"Некоректний ключ: '{key}'. Ключ повинен бути цілим числом")


def validate_text(text):
    if not isinstance(text, str):
        raise TypeError("Вхідні дані повинні бути рядком")
    if len(text) == 0:
        raise ValueError("Вхідний текст не може бути порожнім")
    return text


def shift_char(char, alphabet, shift):
    n = len(alphabet)
    current_index = alphabet.index(char)
    new_index = (current_index + shift) % n
    return alphabet[new_index]


def process_caesar(text, shift):
    result = []

    for char in text:
        if char in UKR_LOWER:
            result.append(shift_char(char, UKR_LOWER, shift))
        elif char in UKR_UPPER:
            result.append(shift_char(char, UKR_UPPER, shift))
        elif char in ENG_LOWER:
            result.append(shift_char(char, ENG_LOWER, shift))
        elif char in ENG_UPPER:
            result.append(shift_char(char, ENG_UPPER, shift))
        else:
            result.append(char)  # Punctuation, digits, spaces, and other symbols

    return "".join(result)


def encrypt(text, key):
    valid_key = validate_key(key)
    valid_text = validate_text(text)
    return process_caesar(valid_text, valid_key)


def decrypt(text, key):
    valid_key = validate_key(key)
    valid_text = validate_text(text)
    return process_caesar(valid_text, -valid_key)


if __name__ == "__main__":
    sample_text = "Привіт, Світ! Hello, World! Єнот їсть ґрунт: 123."
    key = 3

    print(f"Початковий текст:\n{sample_text}\n")

    # Encrypt the text
    encrypted = encrypt(sample_text, key)
    print(f"Зашифрований (ключ = {key}):\n{encrypted}\n")

    # Decrypt back and verify integrity
    decrypted = decrypt(encrypted, key)
    print(f"Розшифрований назад:\n{decrypted}\n")

    assert (decrypted == sample_text), "Помилка: розшифрований текст не збігається з початковим!"
    print("Тест збігу пройшов успішно.")

    # Key validation error handling
    try:
        encrypt("Тест", "три")
    except ValueError as e:
        print(f"Валідація спрацювала коректно: {e}")

    # Empty text validation error handling
    try:
        encrypt("", 3)
    except ValueError as err:
        print(f"Валідація спрацювала коректно: {err}")
