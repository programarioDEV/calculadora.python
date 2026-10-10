"""Transformaciones puras de texto de pantalla."""

import re
from decimal import Decimal

from dunder_calc.config import EASTER_EGGS, EasterEggSettings
from dunder_calc.core.engine import NUMBER_PATTERN

_LAST_NUMBER_RE = re.compile(rf"{NUMBER_PATTERN}%*$")
_TRAILING_INPUT_RE = re.compile(r"[\d.]*$")
_UNARY_CONTEXT = frozenset("+-−×÷*/(")

FLIP_MAP = str.maketrans("0123456789", "OIZEhSgLB6")
CENSORED_FLIPS: tuple[str, ...] = ("BOOB",)
SFW_FLIP = "BOSSES"
FLIP_EGG_DIGITS = "5318008"

RESULT_EGGS: tuple[tuple[Decimal, str], ...] = (
    (Decimal(570), "scranton"),
    (Decimal(1_000_000), "bonus"),
    (Decimal(9), "beet_fact"),
)


def to_display(text: str) -> str:
    """Usa el signo menos tipográfico (−) para un resultado negativo."""
    return "−" + text[1:] if text.startswith("-") else text


def trailing_number(expr: str) -> str:
    """Devuelve el número que se está escribiendo al final de la expresión."""
    match = _TRAILING_INPUT_RE.search(expr)
    return match.group() if match else ""


def toggle_sign(expr: str) -> str:
    """Cambia el signo del último número de la expresión."""
    match = _LAST_NUMBER_RE.search(expr)
    if not match:
        return expr
    before, number = expr[: match.start()], expr[match.start() :]
    if before and before[-1] in "-−":
        prev = before[:-1]
        if not prev or prev[-1] in _UNARY_CONTEXT:
            return prev + number  # Quita un menos unario.
        return prev + "+" + number  # a − b  →  a + b
    if before and before[-1] == "+":
        return before[:-1] + "−" + number
    return before + "−" + number


def flip_text(text: str) -> str:
    """Simula voltear la calculadora: dígitos → letras, en orden inverso."""
    return text.translate(FLIP_MAP)[::-1]


def flip_display(text: str) -> str:
    """Versión volteada apta para el trabajo (aprobada por RR.HH.)."""
    flipped = flip_text(text)
    return SFW_FLIP if any(word in flipped for word in CENSORED_FLIPS) else flipped


def is_flip_egg(text: str) -> bool:
    """Indica si la pantalla contiene el clásico 5318008."""
    return FLIP_EGG_DIGITS in re.sub(r"\D", "", text)


def result_easter_egg(value: Decimal, settings: EasterEggSettings = EASTER_EGGS) -> str | None:
    """Devuelve el nombre del easter egg activado por un resultado, si lo hay."""
    for target, name in RESULT_EGGS:
        if value == target and settings.is_enabled(name):
            return name
    return None
