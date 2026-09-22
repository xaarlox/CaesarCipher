import unittest

from caesar_cipher.core import UniversalByteCaesarCipher


class TestUniversalByteCaesarCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = UniversalByteCaesarCipher()

    def test_bytes_roundtrip(self):
        data = bytes(range(256))
        key = 42

        encrypted = self.cipher.encrypt(data, key)
        decrypted = self.cipher.decrypt(encrypted, key)

        self.assertNotEqual(data, encrypted)
        self.assertEqual(decrypted, data)

    def test_byte_shifts(self):
        data = b"\x00\x01\xfe\xff"
        key = 1
        expected = b"\x01\x02\xff\x00"

        encrypted = self.cipher.encrypt(data, key)
        self.assertEqual(encrypted, expected)

        decrypted = self.cipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, data)


if __name__ == "__main__":
    unittest.main()
