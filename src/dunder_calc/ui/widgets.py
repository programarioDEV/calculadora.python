"""Widgets base: botón con hover, encabezado y pantalla."""

import tkinter as tk
from collections.abc import Callable

from dunder_calc import messages
from dunder_calc.ui.fonts import FontName, FontSet
from dunder_calc.ui.theme import ButtonColors, ButtonKind, Theme


class HoverButton(tk.Button):
    """Botón plano que cambia de color al pasar el ratón."""

    def __init__(
        self,
        master: tk.Misc,
        text: str,
        kind: ButtonKind,
        command: Callable[[], object],
        font: FontSet,
        font_name: FontName = "button",
    ) -> None:
        super().__init__(
            master,
            text=text,
            command=command,
            font=font[font_name],
            relief="flat",
            bd=0,
            highlightthickness=0,
            takefocus=0,
            cursor="hand2",
        )
        self.kind = kind
        self._colors: ButtonColors | None = None
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def apply_theme(self, theme: Theme) -> None:
        self._colors = colors = theme.button(self.kind)
        self.configure(
            bg=colors.bg, fg=colors.fg, activebackground=colors.hover, activeforeground=colors.fg
        )

    def _on_enter(self, _event: tk.Event) -> None:
        if self._colors:
            self.configure(bg=self._colors.hover)

    def _on_leave(self, _event: tk.Event) -> None:
        if self._colors:
            self.configure(bg=self._colors.bg)


class Header(tk.Frame):
    """Título clicable y subtítulo con el nombre del tema."""

    def __init__(self, master: tk.Misc, fonts: FontSet, on_title_click: Callable[[], None]) -> None:
        super().__init__(master)
        self._fonts = fonts
        self._width = 0
        self.columnconfigure(0, weight=1)
        self.title = tk.Label(
            self, text=messages.APP_TITLE, font=fonts["title"], anchor="w", cursor="hand2"
        )
        self.title.grid(row=0, column=0, sticky="ew")
        self.title.bind("<Button-1>", lambda _e: on_title_click())
        self.subtitle = tk.Label(self, font=fonts["subtitle"], anchor="w", justify="left")
        self.subtitle.grid(row=1, column=0, sticky="ew")
        self.bind("<Configure>", self._on_configure)

    def refit(self) -> None:
        """Encoge el título y ajusta el subtítulo para que nunca se corten."""
        if self._width > 1:
            self._fonts.fit_width("title", messages.APP_TITLE, self._width)
            self.subtitle.configure(wraplength=self._width)

    def _on_configure(self, event: tk.Event) -> None:
        self._width = event.width
        self.refit()

    def apply_theme(self, theme: Theme) -> None:
        self.configure(bg=theme.bg)
        self.title.configure(bg=theme.bg, fg=theme.title_fg)
        self.subtitle.configure(bg=theme.bg, fg=theme.subtitle_fg, text=theme.subtitle)


class Display(tk.Frame):
    """Pantalla: operación en curso, resultado y mensajes de estado."""

    def __init__(self, master: tk.Misc, fonts: FontSet) -> None:
        super().__init__(master, padx=16, pady=10)
        self._fonts = fonts
        self.columnconfigure(0, weight=1)
        self.expression = tk.Label(self, font=fonts["expr"], anchor="e")
        self.expression.grid(row=0, column=0, sticky="ew")
        self.result = tk.Label(self, font=fonts["result"], anchor="e")
        self.result.grid(row=1, column=0, sticky="ew")
        self.status = tk.Label(
            self, font=fonts["status"], anchor="w", justify="left", wraplength=360, height=3
        )
        self.status.grid(row=2, column=0, sticky="ew")
        self.bind("<Configure>", self._on_configure)

    def show(self, expression: str, result: str) -> None:
        self.expression.configure(text=expression or " ")
        self.set_result(result)

    def set_result(self, text: str, fit_to: str | None = None) -> None:
        """Muestra `text` ajustando la fuente a la longitud de `fit_to` (o de `text`)."""
        self._fonts.fit_result(len(fit_to or text))
        self.result.configure(text=text)

    def refit(self) -> None:
        self.set_result(str(self.result.cget("text")))

    def set_status(self, text: str) -> None:
        self.status.configure(text=text)

    def _on_configure(self, event: tk.Event) -> None:
        padding = 2 * int(self.cget("padx"))
        self.status.configure(wraplength=max(120, event.width - padding))

    def paint(self, theme: Theme, highlight: bool = False) -> None:
        """Colorea la pantalla; `highlight` invierte a colores de acento."""
        bg = theme.accent if highlight else theme.display_bg
        self.configure(bg=bg)
        if highlight:
            for label in (self.expression, self.result, self.status):
                label.configure(bg=bg, fg=theme.accent_fg)
            return
        self.expression.configure(bg=bg, fg=theme.display_sub)
        self.result.configure(bg=bg, fg=theme.display_fg)
        self.status.configure(bg=bg, fg=theme.accent)
