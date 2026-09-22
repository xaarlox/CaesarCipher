from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from caesar_cipher.core import TextCaesarCipher, UniversalByteCaesarCipher, FileManager

from .editor import Editor
from .statusbar import StatusBar
from .toolbar import build_binary_tools_bar, build_crypto_bar, build_file_toolbar
from .utils import hide_hidden_files_in_dialogs, pick_monospace_font, scale_native_fonts

FILE_TYPES = [("Текстові файли", "*.txt"), ("Усі файли", "*.*")]
ANY_FILE_TYPES = [("Усі файли", "*.*")]

UI_SCALE = 2.0
ctk.set_widget_scaling(UI_SCALE)


class CipherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        scale_native_fonts(UI_SCALE)

        self.title("Шифр Цезаря")
        self.geometry("1600x900")
        self.minsize(1100, 600)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.cipher = TextCaesarCipher()
        self.byte_cipher = UniversalByteCaesarCipher()
        self.current_file: Path | None = None
        self.editor_font = pick_monospace_font(self)
        hide_hidden_files_in_dialogs(self)

        self._build_ui()
        self._bind_shortcuts()

        self.protocol("WM_DELETE_WINDOW", self.exit_app)
        self._update_title()

    def _build_ui(self):
        file_toolbar = build_file_toolbar(
            self,
            on_new=self.new_file,
            on_open=self.open_file,
            on_save=self.save_file,
            on_print=self.print_file,
            on_exit=self.exit_app,
            on_about=self.show_about,
        )
        file_toolbar.pack(fill="x", padx=8, pady=(8, 4))

        crypto_bar, self.key_entry = build_crypto_bar(
            self, on_encrypt=self.encrypt, on_decrypt=self.decrypt,
        )
        crypto_bar.pack(fill="x", padx=8, pady=(0, 4))

        binary_bar = build_binary_tools_bar(
            self, on_encrypt_file=self.encrypt_file, on_decrypt_file=self.decrypt_file,
        )
        binary_bar.pack(fill="x", padx=8, pady=(0, 4))

        self.editor = Editor(self, on_modified=self._update_title)
        self.editor.pack(fill="both", expand=True, padx=8, pady=4)

        self.status = StatusBar(self)
        self.status.pack(fill="x", padx=12, pady=(0, 6))

    def _bind_shortcuts(self):
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-S>", lambda e: self.save_file_as())
        self.bind("<Control-p>", lambda e: self.print_file())
        self.bind("<Control-q>", lambda e: self.exit_app())
        self.bind("<Control-e>", lambda e: self.encrypt())
        self.bind("<Control-d>", lambda e: self.decrypt())

    def _update_title(self):
        name = self.current_file.name if self.current_file else "Без назви"
        star = "*" if self.editor.is_modified() else ""
        self.title(f"{name}{star} (Шифр Цезаря)")

    def _set_status(self, msg: str):
        self.status.set_text(msg)

    def _confirm_discard(self) -> bool:
        if not self.editor.is_modified():
            return True
        answer = messagebox.askyesnocancel("Незбережені зміни", "Зберегти зміни перед продовженням?")
        if answer is None:
            return False
        if answer:
            return self.save_file()
        return True

    def new_file(self):
        if not self._confirm_discard():
            return
        self.current_file = None
        self.editor.set_text("")
        self._set_status("Створено новий файл")
        self._update_title()

    def open_file(self):
        if not self._confirm_discard():
            return
        path = filedialog.askopenfilename(filetypes=FILE_TYPES)
        if not path:
            return
        try:
            content = FileManager.read_file(path)
        except (OSError, UnicodeDecodeError) as err:
            messagebox.showerror("Помилка", f"Не вдалося відкрити файл:\n{err}")
            return
        self.current_file = Path(path)
        self.editor.set_text(content)
        self._set_status(f"Відкрито: {path}")
        self._update_title()

    def save_file(self) -> bool:
        if self.current_file is None:
            return self.save_file_as()
        return self._write(self.current_file)

    def save_file_as(self) -> bool:
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=FILE_TYPES)
        if not path:
            return False
        return self._write(Path(path))

    def _write(self, path: Path) -> bool:
        try:
            FileManager.save_file(path, self.editor.get_text())
        except OSError as err:
            messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{err}")
            return False
        self.current_file = path
        self.editor.mark_modified(False)
        self._set_status(f"Збережено: {path}")
        self._update_title()
        return True

    def print_file(self):
        if self.current_file is None or self.editor.is_modified():
            if not messagebox.askyesno("Друк", "Перед друком файл потрібно зберегти. Зберегти?"):
                return
            if not self.save_file():
                return
        try:
            FileManager.print_file_to_system(self.current_file)
            self._set_status("Файл надіслано на друк")
        except Exception as err:
            messagebox.showerror("Помилка друку", str(err))

    def _run_cipher(self, action, done_msg: str):
        try:
            result = action(self.editor.get_text(), self.key_entry.get().strip())
        except (ValueError, TypeError) as err:
            messagebox.showerror("Помилка", str(err))
            return
        self.editor.set_text(result)
        self.editor.mark_modified(True)
        self._set_status(done_msg)

    def encrypt(self):
        self._run_cipher(self.cipher.encrypt, "Текст зашифровано")

    def decrypt(self):
        self._run_cipher(self.cipher.decrypt, "Текст розшифровано")

    def _process_file(self, action, done_word: str, suggested_suffix: str = "", strip_suffix: str = ""):
        src_path = filedialog.askopenfilename(filetypes=ANY_FILE_TYPES)
        if not src_path:
            return

        name = Path(src_path).name
        if strip_suffix and name.endswith(strip_suffix):
            name = name[: -len(strip_suffix)]
        default_name = name + suggested_suffix

        dest_path = filedialog.asksaveasfilename(initialfile=default_name, filetypes=ANY_FILE_TYPES)
        if not dest_path:
            return

        try:
            data = FileManager.read_bytes(src_path)
            result = action(data, self.key_entry.get().strip())
            FileManager.save_bytes(dest_path, result)
        except (ValueError, TypeError) as err:
            messagebox.showerror("Помилка", str(err))
            return
        except OSError as err:
            messagebox.showerror("Помилка файлу", str(err))
            return

        self._set_status(f"Файл {done_word}: {dest_path}")
        messagebox.showinfo("Готово", f"Файл успішно {done_word} та збережено:\n{dest_path}")

    def encrypt_file(self):
        self._process_file(self.byte_cipher.encrypt, "зашифровано", suggested_suffix=".enc")

    def decrypt_file(self):
        self._process_file(self.byte_cipher.decrypt, "розшифровано", strip_suffix=".enc")

    def show_about(self):
        messagebox.showinfo(
            "Про розробника",
            "Лабораторна робота №1. Шифр Цезаря\n\n"
            "Курс: 4\n"
            "Група: ТВ-33\n"
            "ПІБ: Федоренко Валерія Андріївна\n"
            "GitHub: xaarlox\n"
            "Версія: 1.0",
        )

    def exit_app(self):
        if self._confirm_discard():
            self.destroy()
