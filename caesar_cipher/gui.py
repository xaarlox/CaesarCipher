import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from caesar_cipher.core.ciphers import TextCaesarCipher, UniversalByteCaesarCipher
from caesar_cipher.core.file_manager import FileManager

FILE_TYPES = [("Текстові файли", "*.txt"), ("Усі файли", "*.*")]
ANY_FILE_TYPES = [("Усі файли", "*.*")]

UI_SCALE = 2.0
ctk.set_widget_scaling(UI_SCALE)

NATIVE_FONT_PX = int(14 * UI_SCALE)


def pick_monospace_font(root) -> str:
    available = set(tkfont.families(root))
    for candidate in ("Consolas", "DejaVu Sans Mono", "Liberation Mono", "Noto Sans Mono", "Courier New", "Courier"):
        if candidate in available:
            return candidate
    return tkfont.nametofont("TkFixedFont").actual("family")


def hide_hidden_files_in_dialogs(root) -> None:
    try:
        try:
            root.tk.call("tk_getOpenFile", "-foobarbaz")
        except tk.TclError:
            pass
        root.tk.call("set", "::tk::dialog::file::showHiddenVar", "0")
    except tk.TclError:
        pass


class CipherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont",
                     "TkCaptionFont", "TkSmallCaptionFont", "TkIconFont", "TkTooltipFont"):
            try:
                tkfont.nametofont(name).configure(size=-NATIVE_FONT_PX)
            except tk.TclError:
                pass

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

        self._build_toolbar()
        self._build_editor()
        self._build_statusbar()
        self._build_binary_tools()
        self._bind_shortcuts()

        self.protocol("WM_DELETE_WINDOW", self.exit_app)
        self._update_title()

    def _make_button(self, parent, text, cmd, width=100, **kw):
        b = ctk.CTkButton(parent, text=text, width=width, command=cmd, **kw)
        b.pack(side="left", padx=4, pady=6)
        return b

    def _build_toolbar(self):
        bar = ctk.CTkFrame(self)
        bar.pack(fill="x", padx=8, pady=(8, 4))

        def btn(parent, text, cmd, width=100, **kw):
            b = ctk.CTkButton(parent, text=text, width=width, command=cmd, **kw)
            b.pack(side="left", padx=4, pady=6)
            return b

        btn(bar, "Створити", self.new_file)
        btn(bar, "Відкрити", self.open_file)
        btn(bar, "Зберегти", self.save_file)
        btn(bar, "Друк", self.print_file)

        ctk.CTkButton(bar, text="Вихід", width=90, command=self.exit_app,
                      fg_color="#c62828", hover_color="#8e0000").pack(side="right", padx=4)
        ctk.CTkButton(bar, text="Про розробника", width=130, command=self.show_about,
                      fg_color="gray40", hover_color="gray30").pack(side="right", padx=4)

        crypto = ctk.CTkFrame(self)
        crypto.pack(fill="x", padx=8, pady=(0, 4))

        ctk.CTkLabel(crypto, text="Ключ (ціле число):").pack(side="left", padx=(8, 2))
        self.key_entry = ctk.CTkEntry(crypto, width=140, placeholder_text="Введіть ключ")
        self.key_entry.pack(side="left", padx=4, pady=6)

        btn(crypto, "Зашифрувати", self.encrypt, width=130,
            fg_color="#2e7d32", hover_color="#1b5e20")
        btn(crypto, "Розшифрувати", self.decrypt, width=140,
            fg_color="#ef6c00", hover_color="#e65100")

    def _build_binary_tools(self):
        binary_row = ctk.CTkFrame(self)
        binary_row.pack(fill="x", padx=8, pady=(0, 4))

        ctk.CTkLabel(
            binary_row,
            text="Файл будь-якого формату (jpg, pdf, docx тощо):",
        ).pack(side="left", padx=(8, 2))

        self._make_button(binary_row, "Зашифрувати файл", self.encrypt_file, width=160,
                          fg_color="#00695c", hover_color="#004d40")
        self._make_button(binary_row, "Розшифрувати файл", self.decrypt_file, width=170,
                          fg_color="#4527a0", hover_color="#311b92")

    def _build_editor(self):
        ctk.CTkLabel(self, text="Введіть текст (українська/англійська) або відкрийте файл:",
                     anchor="w").pack(fill="x", padx=12, pady=(4, 0))
        self.textbox = ctk.CTkTextbox(self, wrap="word", font=("Arial", 14), undo=True)
        self.textbox.pack(fill="both", expand=True, padx=8, pady=4)
        self.textbox.bind("<<Modified>>", self._on_modified)

    def _build_statusbar(self):
        self.status = ctk.CTkLabel(self, text="Чекаю на дії...", anchor="w")
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

    def _get_text(self) -> str:
        return self.textbox.get("1.0", "end-1c")

    def _set_text(self, text: str):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text)
        self.textbox.edit_modified(False)

    def _is_modified(self) -> bool:
        return bool(self.textbox.edit_modified())

    def _on_modified(self, _event=None):
        self._update_title()

    def _update_title(self):
        name = self.current_file.name if self.current_file else "Без назви"
        star = "*" if self._is_modified() else ""
        self.title(f"{name}{star} (Шифр Цезаря)")

    def _set_status(self, msg: str):
        self.status.configure(text=msg)

    def _confirm_discard(self) -> bool:
        if not self._is_modified():
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
        self._set_text("")
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
        self._set_text(content)
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
            FileManager.save_file(path, self._get_text())
        except OSError as err:
            messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{err}")
            return False
        self.current_file = path
        self.textbox.edit_modified(False)
        self._set_status(f"Збережено: {path}")
        self._update_title()
        return True

    def print_file(self):
        if self.current_file is None or self._is_modified():
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
            result = action(self._get_text(), self.key_entry.get().strip())
        except (ValueError, TypeError) as err:
            messagebox.showerror("Помилка", str(err))
            return
        self._set_text(result)
        self.textbox.edit_modified(True)
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

        dest_path = filedialog.asksaveasfilename(
            initialfile=default_name, filetypes=ANY_FILE_TYPES
        )
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
        messagebox.showinfo(
            "Готово", f"Файл успішно {done_word} та збережено:\n{dest_path}"
        )

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
