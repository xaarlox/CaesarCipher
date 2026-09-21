from abc import ABC, abstractmethod

from validators import DataValidator, KeyValidator


class BaseCipher(ABC):
    @abstractmethod
    def encrypt(self, data, key):
        pass

    @abstractmethod
    def decrypt(self, data, key):
        pass


class TextCaesarCipher(BaseCipher):
    UKR_LOWER = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
    UKR_UPPER = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
    ENG_LOWER = "abcdefghijklmnopqrstuvwxyz"
    ENG_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def _shift_char(self, char: str, alphabet: str, shift: int) -> str:
        n = len(alphabet)
        current_idx = alphabet.index(char)
        new_idx = (current_idx + shift) % n
        return alphabet[new_idx]

    def _transform(self, text: str, shift: int) -> str:
        result = []

        for char in text:
            if char in self.UKR_LOWER:
                result.append(self._shift_char(char, self.UKR_LOWER, shift))
            elif char in self.UKR_UPPER:
                result.append(self._shift_char(char, self.UKR_UPPER, shift))
            elif char in self.ENG_LOWER:
                result.append(self._shift_char(char, self.ENG_LOWER, shift))
            elif char in self.ENG_UPPER:
                result.append(self._shift_char(char, self.ENG_UPPER, shift))
            else:
                result.append(char)

        return "".join(result)

    def encrypt(self, data: str, key) -> str:
        valid_text = DataValidator.validate_text(data)
        valid_key = KeyValidator.validate(key)
        return self._transform(valid_text, valid_key)

    def decrypt(self, data: str, key) -> str:
        valid_text = DataValidator.validate_text(data)
        valid_key = KeyValidator.validate(key)
        return self._transform(valid_text, -valid_key)
