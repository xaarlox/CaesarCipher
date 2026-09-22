import unittest

from caesar_cipher.core import TextCaesarCipher


class TestTextCaesarCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = TextCaesarCipher()

    def test_english_roundtrip(self):
        original = "The Quick Brown Fox Jumps Over 13 Lazy Dogs!"
        key = 4
        encrypted = self.cipher.encrypt(original, key)
        decrypted = self.cipher.decrypt(encrypted, key)

        self.assertNotEqual(original, encrypted)
        self.assertEqual(decrypted, original)

    def test_ukrainian_specific_letters(self):
        original = "Юний ґазда з'їв яблуко біля єнота!"
        key = 7
        encrypted = self.cipher.encrypt(original, key)
        decrypted = self.cipher.decrypt(encrypted, key)

        self.assertEqual(decrypted, original)

    def test_case_and_punctuation_preservation(self):
        original = "Hello, Світ! 123... @#$ \n\t"
        key = 5
        encrypted = self.cipher.encrypt(original, key)
        decrypted = self.cipher.decrypt(encrypted, key)

        self.assertEqual(decrypted, original)
        self.assertIn("123... @#$", encrypted)

    def test_modular_wrap_and_large_keys(self):
        original = "АБВГ abc"
        key = 33 * 26 + 1
        encrypted = self.cipher.encrypt(original, key)
        decrypted = self.cipher.decrypt(encrypted, key)

        self.assertEqual(decrypted, original)

    def test_negative_key(self):
        original = "Київ та London"
        key = -10
        encrypted = self.cipher.encrypt(original, key)
        decrypted = self.cipher.decrypt(encrypted, key)

        self.assertEqual(decrypted, original)


if __name__ == "__main__":
    unittest.main()
