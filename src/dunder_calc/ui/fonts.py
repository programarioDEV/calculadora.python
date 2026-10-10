"""Tipografías escalables según el tamaño de la ventana."""

import tkinter as tk
from tkinter import font as tkfont
from typing import Literal

FontName = Literal["title", "subtitle", "expr", "result", "status", "button", "small"]

FONT_CANDIDATES: tuple[str, ...] = (
    "Segoe UI",
    "Helvetica Neue",
    "Inter",
    "Cantarell",
    "Ubuntu",
    "DejaVu Sans",
    "Liberation Sans",
    "Helvetica",
    "Arial",
)
BASE_SIZES: dict[FontName, int] = {
    "title": 18,
    "subtitle": 10,
    "expr": 13,
    "result": 36,
    "status": 11,
    "button": 16,
    "small": 11,
}
_BOLD: frozenset[FontName] = frozenset({"title", "result"})
_ITALIC: frozenset[FontName] = frozenset({"status"})
_SELF_FITTED: frozenset[FontName] = frozenset({"title", "result"})
RESULT_FIT_CHARS = 11
MIN_SIZE = 8
MIN_RESULT_SIZE = 12


def pick_family(root: tk.Misc) -> str:
    """Primera fuente limpia disponible, o la fuente por defecto de Tk."""
    available = set(tkfont.families(root))
    default = str(tkfont.nametofont("TkDefaultFont").actual("family"))
    return next((family for family in FONT_CANDIDATES if family in available), default)


class FontSet:
    """Conjunto de fuentes con nombre que se reescala con la ventana."""

    def __init__(self, root: tk.Misc) -> None:
        family = pick_family(root)
        self.scale = 1.0
        self._fonts: dict[FontName, tkfont.Font] = {
            name: tkfont.Font(
                root=root,
                family=family,
                size=size,
                weight="bold" if name in _BOLD else "normal",
                slant="italic" if name in _ITALIC else "roman",
            )
            for name, size in BASE_SIZES.items()
        }

    def __getitem__(self, name: FontName) -> tkfont.Font:
        return self._fonts[name]

    def rescale(self, scale: float) -> bool:
        """Aplica una nueva escala; devuelve False si el cambio es despreciable."""
        if abs(scale - self.scale) < 0.04:
            return False
        self.scale = scale
        for name, font in self._fonts.items():
            if name not in _SELF_FITTED:
                font.configure(size=max(MIN_SIZE, int(BASE_SIZES[name] * scale)))
        return True

    def fit_result(self, length: int) -> None:
        """Reduce la fuente del resultado si el texto es largo."""
        size = int(BASE_SIZES["result"] * self.scale)
        if length > RESULT_FIT_CHARS:
            size = max(MIN_RESULT_SIZE, int(size * RESULT_FIT_CHARS / length))
        self._fonts["result"].configure(size=size)

    def fit_width(self, name: FontName, text: str, max_width: int) -> None:
        """Usa el mayor tamaño (hasta el escalado) en el que `text` cabe en `max_width` px."""
        font = self._fonts[name]
        size = max(MIN_SIZE, int(BASE_SIZES[name] * self.scale))
        font.configure(size=size)
        while size > MIN_SIZE and font.measure(text) > max_width:
            size -= 1
            font.configure(size=size)
