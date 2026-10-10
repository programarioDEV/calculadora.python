"""Lógica pura de la calculadora: no importa tkinter."""

from dunder_calc.core.engine import CalcError, DivisionByZeroError, evaluate, format_result
from dunder_calc.core.model import CalculatorModel, Event, HistoryEntry

__all__ = [
    "CalcError",
    "CalculatorModel",
    "DivisionByZeroError",
    "Event",
    "HistoryEntry",
    "evaluate",
    "format_result",
]
