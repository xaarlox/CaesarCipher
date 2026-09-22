class KeyValidator:
    @staticmethod
    def validate(key) -> int:
        if isinstance(key, bool):
            raise ValueError("Ключ не може бути логічним значенням (True/False).")
        try:
            return int(key)
        except (TypeError, ValueError):
            raise ValueError(f"Некоректний ключ '{key}'. Ключ має бути цілим числом.")


class DataValidator:
    @staticmethod
    def validate_text(text: str) -> str:
        if not isinstance(text, str):
            raise TypeError(f"Очікувався рядок, отримано {type(text).__name__}.")
        if len(text) == 0:
            raise ValueError("Текст для обробки не може бути порожнім.")
        return text
