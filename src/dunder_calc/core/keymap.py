"""Traducción de teclas y botones a comandos de la calculadora."""

from dataclasses import dataclass
from enum import Enum, auto


class Action(Enum):
    """Acciones que puede ejecutar la calculadora."""

    DIGIT = auto()
    DOT = auto()
    OPERATOR = auto()
    PERCENT = auto()
    TOGGLE_SIGN = auto()
    BACKSPACE = auto()
    CLEAR = auto()
    EQUALS = auto()
    FLIP = auto()
    HISTORY = auto()


@dataclass(frozen=True, slots=True)
class Command:
    """Acción con su argumento opcional (dígito u operador)."""

    action: Action
    arg: str = ""


OPERATORS = "+−×÷"
_KEY_OPERATORS = {"+": "+", "-": "−", "*": "×", "/": "÷"}
_BUTTON_ACTIONS = {
    "C": Action.CLEAR,
    "⌫": Action.BACKSPACE,
    "%": Action.PERCENT,
    "±": Action.TOGGLE_SIGN,
    ".": Action.DOT,
    "=": Action.EQUALS,
}
_KEYSYM_ACTIONS = {
    "Return": Action.EQUALS,
    "KP_Enter": Action.EQUALS,
    "Escape": Action.CLEAR,
    "BackSpace": Action.BACKSPACE,
}
_CHAR_ACTIONS = {
    ".": Action.DOT,
    ",": Action.DOT,
    "%": Action.PERCENT,
    "=": Action.EQUALS,
    "f": Action.FLIP,
    "h": Action.HISTORY,
}


def map_button(label: str) -> Command:
    """Comando asociado a la etiqueta de un botón del teclado en pantalla."""
    if label.isdigit():
        return Command(Action.DIGIT, label)
    if label in OPERATORS:
        return Command(Action.OPERATOR, label)
    return Command(_BUTTON_ACTIONS[label])


def map_key(char: str, keysym: str) -> Command | None:
    """Comando asociado a una tecla física, o None si no tiene función."""
    if len(char) == 1 and char.isdigit():
        return Command(Action.DIGIT, char)
    if char in _KEY_OPERATORS:
        return Command(Action.OPERATOR, _KEY_OPERATORS[char])
    if keysym in _KEYSYM_ACTIONS:
        return Command(_KEYSYM_ACTIONS[keysym])
    if action := _CHAR_ACTIONS.get(char.lower()):
        return Command(action)
    return None
