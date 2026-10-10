"""Punto de entrada: `python -m dunder_calc`."""

import sys

from dunder_calc import messages


def main() -> int:
    """Abre la calculadora; devuelve 1 si tkinter no está disponible."""
    try:
        import tkinter as tk

        from dunder_calc.ui.app import CalculatorApp
    except ImportError:
        print(messages.NO_TKINTER, file=sys.stderr)
        return 1
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
