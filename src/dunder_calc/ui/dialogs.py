"""Ventanas emergentes."""

import tkinter as tk

from dunder_calc import messages
from dunder_calc.ui.fonts import FontSet
from dunder_calc.ui.theme import ButtonKind, Theme
from dunder_calc.ui.widgets import HoverButton


def show_bonus_dialog(root: tk.Misc, theme: Theme, fonts: FontSet) -> tk.Toplevel:
    """Ventana del bono de fin de año (se cierra con el botón o con Esc)."""
    win = tk.Toplevel(root, bg=theme.panel, padx=24, pady=20)
    win.title(messages.BONUS_WINDOW_TITLE)
    win.transient(root.winfo_toplevel())
    win.resizable(False, False)
    tk.Label(
        win, text=messages.BONUS_HEADING, font=fonts["title"], bg=theme.panel, fg=theme.title_fg
    ).pack(pady=(0, 8))
    tk.Label(
        win,
        text=messages.BONUS_BODY,
        font=fonts["small"],
        justify="center",
        bg=theme.panel,
        fg=theme.button(ButtonKind.NUM).fg,
    ).pack(pady=(0, 14))
    button = HoverButton(win, messages.BONUS_BUTTON, ButtonKind.EQ, win.destroy, fonts, "small")
    button.configure(padx=14, pady=6)
    button.apply_theme(theme)
    button.pack()
    win.bind("<Escape>", lambda _e: win.destroy())
    return win
