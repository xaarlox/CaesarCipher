class KeyValidator:
    @staticmethod
    def validate(key) -> int:
        if isinstance(key, bool):
            raise ValueError("Key cannot be a boolean value.")
        try:
            return int(key)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid key '{key}'. Key must be an integer.")


class DataValidator:
    @staticmethod
    def validate_text(text: str) -> str:
        if not isinstance(text, str):
            raise TypeError(f"Expected a string, got {type(text).__name__} instead.")
        if len(text) == 0:
            raise ValueError("Input text cannot be empty.")
        return text
