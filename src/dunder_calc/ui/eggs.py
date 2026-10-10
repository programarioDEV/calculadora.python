"""Efectos visuales de los easter eggs (uno por método, activables en config)."""

import random
import tkinter as tk
from collections.abc import Callable
from typing import Protocol

from dunder_calc import messages
from dunder_calc.config import EasterEggSettings
from dunder_calc.core.transforms import SFW_FLIP, is_flip_egg
from dunder_calc.ui.animator import Animator
from dunder_calc.ui.dialogs import show_bonus_dialog
from dunder_calc.ui.fonts import FontSet
from dunder_calc.ui.theme import DEFAULT_THEME, Theme
from dunder_calc.ui.widgets import Display


class ThemeHost(Protocol):
    """Quien gestiona el tema activo (la aplicación)."""

    @property
    def theme(self) -> Theme: ...

    def apply_theme(self, name: str) -> None: ...


class EasterEggs:
    """Cada método devuelve True si el easter egg se mostró."""

    def __init__(
        self,
        root: tk.Misc,
        host: ThemeHost,
        display: Display,
        animator: Animator,
        fonts: FontSet,
        settings: EasterEggSettings,
    ) -> None:
        self._root = root
        self._host = host
        self._display = display
        self._animator = animator
        self._fonts = fonts
        self._settings = settings
        self._bonus_window: tk.Toplevel | None = None

    def by_name(self, name: str) -> Callable[[], bool] | None:
        """Easter egg de resultado (scranton, bonus, beet_fact) por nombre."""
        eggs: dict[str, Callable[[], bool]] = {
            "scranton": self.scranton,
            "bonus": self.bonus,
            "beet_fact": self.beet_fact,
        }
        return eggs.get(name)

    def divide_by_zero(self) -> bool:
        """1 · Michael opina sobre la división entre cero."""
        if not self._settings.divide_by_zero:
            return False
        self._display.set_result(messages.DIVIDE_BY_ZERO_RESULT)
        self._display.set_status("Michael: " + random.choice(messages.MICHAEL_ZERO_LINES))
        return True

    def scranton(self) -> bool:
        """2 · Resultado 570: Scranton, PA con destello."""
        if not self._settings.scranton:
            return False
        self._display.set_status(messages.SCRANTON)
        self._blink_display()
        return True

    def bonus(self) -> bool:
        """3 · Resultado 1 000 000: ventana de bono de fin de año."""
        if not self._settings.bonus:
            return False
        if self._bonus_window is not None and self._bonus_window.winfo_exists():
            self._bonus_window.lift()
        else:
            self._bonus_window = show_bonus_dialog(self._root, self._host.theme, self._fonts)
        self._display.set_status(messages.BONUS_STATUS)
        return True

    def flip(self, shown: str) -> bool:
        """4 · 5318008 volteado, en versión apta para la oficina."""
        if not self._settings.flip or not is_flip_egg(shown):
            return False
        self._display.set_result("↻", fit_to=SFW_FLIP)
        self._animator.schedule(300, lambda: self._display.set_result(SFW_FLIP))
        self._display.set_status(messages.FLIP_EGG)
        return True

    def beet_fact(self) -> bool:
        """5 · Resultado 9: dato serio de Dwight sobre remolacha."""
        if not self._settings.beet_fact:
            return False
        self._display.set_status("Dato de Dwight: " + random.choice(messages.DWIGHT_BEET_FACTS))
        return True

    def jello(self) -> bool:
        """6 · Cinco clics en el título: tema Jell-O (repetir para salir)."""
        if not self._settings.jello:
            return False
        return self._toggle_theme("jello", messages.JELLO_ON, messages.JELLO_OFF)

    def konami(self) -> bool:
        """7 · Código Konami: Michael Scott Paper Company (repetir para salir)."""
        if not self._settings.konami:
            return False
        return self._toggle_theme("mspc", messages.MSPC_ON, messages.MSPC_OFF)

    def bankruptcy(self) -> bool:
        """8 · Diez C seguidas: «¡DECLARO BANCARROTA!» animado."""
        if not self._settings.bankruptcy:
            return False
        text = messages.BANKRUPTCY_TEXT
        duration = self._animator.typewriter(
            text, lambda part: self._display.set_result(part, fit_to=text)
        )
        self._animator.schedule(duration + 150, self._blink_display)
        self._display.set_status(messages.BANKRUPTCY_STATUS)
        return True

    # ------------------------------------------------------------ internos
    def _toggle_theme(self, name: str, on_message: str, off_message: str) -> bool:
        self._animator.cancel_all()
        leaving = self._host.theme.name == name
        self._host.apply_theme(DEFAULT_THEME if leaving else name)
        self._display.set_status(off_message if leaving else on_message)
        return True

    def _blink_display(self) -> None:
        self._animator.blink(
            on=lambda: self._display.paint(self._host.theme, highlight=True),
            off=lambda: self._display.paint(self._host.theme),
        )
