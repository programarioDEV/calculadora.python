"""Paneles compuestos: teclado en cuadrícula e historial."""

import tkinter as tk
from collections.abc import Callable
from functools import partial

from dunder_calc import messages
from dunder_calc.core.keymap import OPERATORS, Action, Command, map_button
from dunder_calc.ui.fonts import FontSet
from dunder_calc.ui.theme import ButtonKind, Theme
from dunder_calc.ui.widgets import HoverButton

KEYPAD_LAYOUT: tuple[tuple[str, ...], ...] = (
    ("C", "⌫", "%", "÷"),
    ("7", "8", "9", "×"),
    ("4", "5", "6", "−"),
    ("1", "2", "3", "+"),
    ("±", "0", ".", "="),
)


def kind_for(label: str) -> ButtonKind:
    """Familia de color de un botón según su etiqueta."""
    if label.isdigit() or label == ".":
        return ButtonKind.NUM
    if label in OPERATORS:
        return ButtonKind.OP
    return ButtonKind.EQ if label == "=" else ButtonKind.FN


class Keypad(tk.Frame):
    """Cuadrícula de botones con filas y columnas uniformes."""

    def __init__(
        self, master: tk.Misc, fonts: FontSet, on_command: Callable[[Command], None]
    ) -> None:
        super().__init__(master)
        self.buttons: list[HoverButton] = []
        rows = len(KEYPAD_LAYOUT) + 1
        for r in range(rows):
            self.rowconfigure(r, weight=1, uniform="row")
        for c in range(4):
            self.columnconfigure(c, weight=1, uniform="col")

        for r, row in enumerate(KEYPAD_LAYOUT):
            for c, label in enumerate(row):
                command = partial(on_command, map_button(label))
                btn = self._add(label, kind_for(label), command, fonts)
                btn.grid(row=r, column=c, padx=3, pady=3, ipady=6, sticky="nsew")

        extras = ((messages.FLIP_BUTTON, Action.FLIP), (messages.HISTORY_BUTTON, Action.HISTORY))
        for i, (label, action) in enumerate(extras):
            command = partial(on_command, Command(action))
            btn = self._add(label, ButtonKind.FN, command, fonts, small=True)
            btn.grid(
                row=rows - 1, column=i * 2, columnspan=2, padx=3, pady=3, ipady=4, sticky="nsew"
            )

    def _add(
        self,
        label: str,
        kind: ButtonKind,
        command: Callable[[], None],
        fonts: FontSet,
        small: bool = False,
    ) -> HoverButton:
        btn = HoverButton(self, label, kind, command, fonts, "small" if small else "button")
        self.buttons.append(btn)
        return btn

    def apply_theme(self, theme: Theme) -> None:
        self.configure(bg=theme.bg)
        for btn in self.buttons:
            btn.apply_theme(theme)


class HistoryPanel(tk.Frame):
    """Lista de operaciones de la sesión; doble clic recupera una."""

    def __init__(
        self,
        master: tk.Misc,
        fonts: FontSet,
        on_pick: Callable[[int], None],
        on_clear: Callable[[], None],
    ) -> None:
        super().__init__(master, padx=8, pady=8)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.title = tk.Label(self, text=messages.HISTORY_TITLE, font=fonts["small"], anchor="w")
        self.title.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6))
        self.listbox = tk.Listbox(
            self, font=fonts["small"], activestyle="none", borderwidth=0, highlightthickness=0
        )
        self.listbox.grid(row=1, column=0, sticky="nsew")
        self.listbox.bind("<Double-Button-1>", lambda _e: self._pick(on_pick))
        self.scrollbar = tk.Scrollbar(self, command=self.listbox.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.clear_button = HoverButton(
            self, messages.HISTORY_CLEAR, ButtonKind.FN, on_clear, fonts, "small"
        )
        self.clear_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 0))

    def add(self, entry: str) -> None:
        self.listbox.insert("end", entry)
        self.listbox.see("end")

    def clear(self) -> None:
        self.listbox.delete(0, "end")

    def _pick(self, on_pick: Callable[[int], None]) -> None:
        if selection := self.listbox.curselection():  # type: ignore[no-untyped-call]
            on_pick(int(selection[0]))

    def apply_theme(self, theme: Theme) -> None:
        num = theme.button(ButtonKind.NUM)
        op = theme.button(ButtonKind.OP)
        fn = theme.button(ButtonKind.FN)
        self.configure(bg=theme.panel)
        self.title.configure(bg=theme.panel, fg=theme.title_fg)
        self.listbox.configure(
            bg=theme.panel, fg=num.fg, selectbackground=op.bg, selectforeground=op.fg
        )
        self.scrollbar.configure(bg=fn.bg, troughcolor=theme.panel, activebackground=fn.hover)
        self.clear_button.apply_theme(theme)
