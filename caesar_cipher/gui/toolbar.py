import customtkinter as ctk

from .colors import Colors


def _button(parent, text, cmd, width=100, **kw):
    b = ctk.CTkButton(parent, text=text, width=width, command=cmd, **kw)
    b.pack(side="left", padx=4, pady=6)
    return b


def build_file_toolbar(parent, *, on_new, on_open, on_save, on_print, on_exit, on_about):
    bar = ctk.CTkFrame(parent)

    _button(bar, "Створити", on_new)
    _button(bar, "Відкрити", on_open)
    _button(bar, "Зберегти", on_save)
    _button(bar, "Друк", on_print)

    ctk.CTkButton(
        bar, text="Вихід", width=90, command=on_exit, fg_color=Colors.DANGER, hover_color=Colors.DANGER_HOVER,
    ).pack(side="right", padx=4)

    ctk.CTkButton(
        bar, text="Про розробника", width=130, command=on_about, fg_color=Colors.NEUTRAL,
        hover_color=Colors.NEUTRAL_HOVER,
    ).pack(side="right", padx=4)

    return bar


def build_crypto_bar(parent, *, on_encrypt, on_decrypt):
    bar = ctk.CTkFrame(parent)

    ctk.CTkLabel(bar, text="Ключ (ціле число):").pack(side="left", padx=(8, 2))
    key_entry = ctk.CTkEntry(bar, width=140, placeholder_text="Введіть ключ")
    key_entry.pack(side="left", padx=4, pady=6)

    _button(
        bar, "Зашифрувати", on_encrypt, width=130,
        fg_color=Colors.SUCCESS, hover_color=Colors.SUCCESS_HOVER,
    )
    _button(
        bar, "Розшифрувати", on_decrypt, width=140,
        fg_color=Colors.WARNING, hover_color=Colors.WARNING_HOVER,
    )

    return bar, key_entry


def build_binary_tools_bar(parent, *, on_encrypt_file, on_decrypt_file):
    bar = ctk.CTkFrame(parent)

    ctk.CTkLabel(
        bar, text="Файл будь-якого формату (jpg, pdf, docx тощо):",
    ).pack(side="left", padx=(8, 2))

    _button(
        bar, "Зашифрувати файл", on_encrypt_file, width=160,
        fg_color=Colors.TEAL, hover_color=Colors.TEAL_HOVER,
    )
    _button(
        bar, "Розшифрувати файл", on_decrypt_file, width=170,
        fg_color=Colors.PURPLE, hover_color=Colors.PURPLE_HOVER,
    )

    return bar
