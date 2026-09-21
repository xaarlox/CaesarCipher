import os
import subprocess
from pathlib import Path
import platform


class FileManager:
    @staticmethod
    def create_file(file_path: str | Path, initial_content: str = "") -> None:
        FileManager.save_file(file_path, initial_content)

    @staticmethod
    def read_file(file_path: str | Path) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def save_file(file_path: str | Path, content: str) -> None:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def print_file_to_system(file_path: str | Path) -> bool:
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Cannot print: file {file_path} does not exist.")

        current_os = platform.system()
        try:
            if current_os == "Windows":
                os.startfile(str(path), "print")
                return True
            elif current_os == "Linux":
                subprocess.run(["lpr", str(path)], check=True)
                return True
            elif current_os == "Darwin":
                subprocess.run(["lp", str(path)], check=True)
                return True
            else:
                raise NotImplementedError(f"Printing is not supported on {current_os}.")
        except NotImplementedError:
            raise
        except Exception as err:
            raise RuntimeError(f"System printing error: {err}") from err
