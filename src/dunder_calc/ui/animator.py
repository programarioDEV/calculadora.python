"""Animaciones cancelables basadas en `after` de Tk."""

import tkinter as tk
from collections.abc import Callable
from contextlib import suppress
from functools import partial


class Animator:
    """Programa pasos de animación y permite cancelarlos todos a la vez."""

    def __init__(self, widget: tk.Misc, on_cancel: Callable[[], None] | None = None) -> None:
        self._widget = widget
        self._on_cancel = on_cancel
        self._jobs: list[str] = []

    def schedule(self, delay_ms: int, func: Callable[[], None]) -> None:
        self._jobs.append(self._widget.after(delay_ms, func))

    def cancel_all(self) -> None:
        """Detiene las animaciones pendientes y restaura el estado visual."""
        for job in self._jobs:
            with suppress(tk.TclError):
                self._widget.after_cancel(job)
        self._jobs.clear()
        if self._on_cancel:
            self._on_cancel()

    def blink(
        self,
        on: Callable[[], None],
        off: Callable[[], None],
        times: int = 6,
        interval_ms: int = 140,
    ) -> None:
        """Alterna `on`/`off` varias veces y termina en `off`."""
        for i in range(times):
            self.schedule(i * interval_ms, on if i % 2 == 0 else off)
        self.schedule(times * interval_ms, off)

    def typewriter(self, text: str, render: Callable[[str], None], delay_ms: int = 70) -> int:
        """Muestra `text` letra a letra; devuelve la duración total en ms."""
        for i in range(1, len(text) + 1):
            self.schedule(i * delay_ms, partial(render, text[:i]))
        return len(text) * delay_ms
