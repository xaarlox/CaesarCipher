import customtkinter as ctk


class Editor:
    def __init__(self, parent, *, on_modified=None):
        self._on_modified = on_modified

        self.frame = ctk.CTkFrame(parent, fg_color="transparent")

        ctk.CTkLabel(
            self.frame,
            text="Введіть текст (українська/англійська) або відкрийте файл:",
            anchor="w",
        ).pack(fill="x")

        self.textbox = ctk.CTkTextbox(self.frame, wrap="word", font=("Arial", 14), undo=True)
        self.textbox.pack(fill="both", expand=True, pady=4)
        self.textbox.bind("<<Modified>>", self._handle_modified)

    def pack(self, **kw):
        self.frame.pack(**kw)

    def _handle_modified(self, _event=None):
        if self._on_modified:
            self._on_modified()

    def get_text(self) -> str:
        return self.textbox.get("1.0", "end-1c")

    def set_text(self, text: str) -> None:
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text)
        self.textbox.edit_modified(False)

    def is_modified(self) -> bool:
        return bool(self.textbox.edit_modified())

    def mark_modified(self, value: bool = True) -> None:
        self.textbox.edit_modified(value)
