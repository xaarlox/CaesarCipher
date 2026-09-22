import unittest

from caesar_cipher.core import KeyValidator, DataValidator


class TestKeyValidator(unittest.TestCase):
    def test_valid_key(self):
        self.assertEqual(KeyValidator.validate(3), 3)
        self.assertEqual(KeyValidator.validate(-5), -5)
        self.assertEqual(KeyValidator.validate("14"), 14)

    def test_rejects_bool(self):
        with self.assertRaises(ValueError):
            KeyValidator.validate(True)
        with self.assertRaises(ValueError):
            KeyValidator.validate(False)

    def test_rejects_non_integers(self):
        invalid_keys = ["abc", "3.14", None, [], {}, "3a"]

        for key in invalid_keys:
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    KeyValidator.validate(key)


class TestDataValidator(unittest.TestCase):
    def test_validate_text(self):
        self.assertEqual(DataValidator.validate_text("Привіт"), "Привіт")

        with self.assertRaises(ValueError):
            DataValidator.validate_text("")

        with self.assertRaises(TypeError):
            DataValidator.validate_text(12345)

    def test_validate_bytes(self):
        valid_bytes = b"sample_bytes"
        self.assertEqual(DataValidator.validate_bytes(valid_bytes), valid_bytes)
        self.assertEqual(DataValidator.validate_bytes(bytearray(b"test")), b"test")

        with self.assertRaises(ValueError):
            DataValidator.validate_bytes(b"")

        with self.assertRaises(TypeError):
            DataValidator.validate_bytes("рядок замість байтів")


if __name__ == "__main__":
    unittest.main()
