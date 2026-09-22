import tkinter as tk
import tkinter.font as tkfont


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


def scale_native_fonts(scale: float) -> None:
    px = int(14 * scale)
    for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont",
                 "TkCaptionFont", "TkSmallCaptionFont", "TkIconFont", "TkTooltipFont"):
        try:
            tkfont.nametofont(name).configure(size=-px)
        except tk.TclError:
            pass
