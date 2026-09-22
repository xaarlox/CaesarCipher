import tempfile
import unittest
from pathlib import Path

from caesar_cipher.core import FileManager


class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_text_file_lifecycle(self):
        file_path = self.dir_path / "sample.txt"
        content = "Секретний текст для лаби."

        FileManager.create_file(file_path, content)
        self.assertTrue(file_path.exists())

        read_back = FileManager.read_file(file_path)
        self.assertEqual(read_back, content)

    def test_binary_file_lifecycle(self):
        bin_path = self.dir_path / "sample.bin"
        raw_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"

        FileManager.save_bytes(bin_path, raw_bytes)
        self.assertTrue(bin_path.exists())

        read_back = FileManager.read_bytes(bin_path)
        self.assertEqual(read_back, raw_bytes)

    def test_read_nonexistent_file_raises(self):
        missing_path = self.dir_path / "not_found.txt"
        with self.assertRaises(FileNotFoundError):
            FileManager.read_file(missing_path)


if __name__ == "__main__":
    unittest.main()
