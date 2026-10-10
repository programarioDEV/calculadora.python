"""Configuración general: límites de entrada e interruptores de easter eggs."""

from dataclasses import dataclass

MAX_EXPR_LEN = 200
MAX_INPUT_LEN = 40
CLEAR_STREAK_TARGET = 10
TITLE_CLICKS_TARGET = 5
TITLE_CLICKS_WINDOW_S = 2.0
KONAMI_CODE: tuple[str, ...] = (
    "up",
    "up",
    "down",
    "down",
    "left",
    "right",
    "left",
    "right",
    "b",
    "a",
)


@dataclass
class EasterEggSettings:
    """Interruptores de easter eggs: pon un campo en False para desactivarlo."""

    divide_by_zero: bool = True
    scranton: bool = True
    bonus: bool = True
    flip: bool = True
    beet_fact: bool = True
    jello: bool = True
    konami: bool = True
    bankruptcy: bool = True

    def is_enabled(self, name: str) -> bool:
        """Indica si el easter egg `name` existe y está activo."""
        return bool(getattr(self, name, False))


EASTER_EGGS = EasterEggSettings()
