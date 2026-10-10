"""Dunder Mifflin Calculator: calculadora tkinter con temática de The Office."""

from dunder_calc.core import CalcError, DivisionByZeroError, evaluate, format_result

__version__ = "2.0.0"
__all__ = ["CalcError", "DivisionByZeroError", "__version__", "evaluate", "format_result"]
