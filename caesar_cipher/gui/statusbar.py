import customtkinter as ctk


class StatusBar:
    def __init__(self, parent):
        self.label = ctk.CTkLabel(parent, text="Чекаю на дії...", anchor="w")

    def pack(self, **kw):
        self.label.pack(**kw)

    def set_text(self, msg: str) -> None:
        self.label.configure(text=msg)
