"""Estado de la calculadora y reglas de edición (independiente de la interfaz)."""

from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum, auto

from dunder_calc.config import CLEAR_STREAK_TARGET, MAX_INPUT_LEN
from dunder_calc.core.engine import CalcError, DivisionByZeroError, evaluate, format_result
from dunder_calc.core.keymap import OPERATORS, Action, Command
from dunder_calc.core.transforms import to_display, toggle_sign, trailing_number


class Event(Enum):
    """Resultado de aplicar un comando al modelo."""

    UPDATED = auto()
    IGNORED = auto()
    INPUT_FULL = auto()
    INVALID = auto()
    DIVIDE_BY_ZERO = auto()
    EVALUATED = auto()
    CLEAR_STREAK = auto()


@dataclass(frozen=True, slots=True)
class HistoryEntry:
    """Operación completada del historial."""

    expression: str
    result: str

    def __str__(self) -> str:
        return f"{self.expression} = {self.result}"


@dataclass
class CalculatorModel:
    """Expresión en curso, resultado parcial e historial de la sesión."""

    expr: str = ""
    result: str = "0"
    last_expr: str = ""
    just_evaluated: bool = False
    last_value: Decimal | None = None
    clear_streak: int = 0
    history: list[HistoryEntry] = field(default_factory=list)

    @property
    def expression_line(self) -> str:
        """Texto de la línea superior de la pantalla."""
        if self.just_evaluated and self.last_expr:
            return f"{self.last_expr} ="
        return self.expr

    def apply(self, command: Command) -> Event:
        """Aplica un comando de edición; las acciones de interfaz se ignoran."""
        handlers: dict[Action, Callable[[], Event]] = {
            Action.DIGIT: lambda: self.digit(command.arg),
            Action.OPERATOR: lambda: self.operator(command.arg),
            Action.DOT: self.dot,
            Action.PERCENT: self.percent,
            Action.TOGGLE_SIGN: self.toggle_sign,
            Action.BACKSPACE: self.backspace,
            Action.CLEAR: self.clear,
            Action.EQUALS: self.equals,
        }
        handler = handlers.get(command.action)
        return handler() if handler else Event.IGNORED

    # ------------------------------------------------------------ edición
    def digit(self, digit: str) -> Event:
        if len(digit) != 1 or not digit.isdigit():
            return Event.IGNORED
        self._start_new_number()
        if len(self.expr) >= MAX_INPUT_LEN:
            return Event.INPUT_FULL
        self._close_percent()
        replace_zero = trailing_number(self.expr) == "0"
        self.expr = (self.expr[:-1] if replace_zero else self.expr) + digit
        return self._preview()

    def dot(self) -> Event:
        self._start_new_number()
        if len(self.expr) >= MAX_INPUT_LEN:
            return Event.INPUT_FULL
        self._close_percent()
        current = trailing_number(self.expr)
        if "." in current:
            return Event.IGNORED
        self.expr += "." if current else "0."
        return self._preview()

    def operator(self, op: str) -> Event:
        if op not in OPERATORS:
            return Event.IGNORED
        self._continue_expression()
        if len(self.expr) >= MAX_INPUT_LEN:
            return Event.INPUT_FULL
        if not self.expr:
            self.expr = "−" if op == "−" else "0" + op
        elif self.expr[-1] not in OPERATORS:
            self.expr += op
        elif op == "−" and self.expr[-1] in "×÷":
            self.expr += op  # Menos unario: 5×−3
        else:
            stripped = self.expr.rstrip(OPERATORS)
            self.expr = stripped + op if stripped else ("−" if op == "−" else "")
        return self._preview()

    def percent(self) -> Event:
        self.clear_streak = 0
        if not self.expr or not (self.expr[-1].isdigit() or self.expr[-1] == "."):
            return Event.IGNORED
        self._continue_expression()
        self.expr += "%"
        return self._preview()

    def toggle_sign(self) -> Event:
        self.clear_streak = 0
        if not self.expr:
            return Event.IGNORED
        self._continue_expression()
        self.expr = toggle_sign(self.expr)
        return self._preview()

    def backspace(self) -> Event:
        self.clear_streak = 0
        if self.just_evaluated:
            self.expr, self.just_evaluated = "", False
        else:
            self.expr = self.expr[:-1]
        return self._preview()

    def clear(self) -> Event:
        """Borra todo; la décima vez seguida dispara CLEAR_STREAK."""
        self.expr, self.result, self.last_expr = "", "0", ""
        self.just_evaluated = False
        self.clear_streak += 1
        if self.clear_streak >= CLEAR_STREAK_TARGET:
            self.clear_streak = 0
            return Event.CLEAR_STREAK
        return Event.UPDATED

    def equals(self) -> Event:
        self.clear_streak = 0
        if not self.expr or self.just_evaluated:
            return Event.IGNORED
        expr = self.expr
        try:
            value = evaluate(expr)
        except DivisionByZeroError:
            self.expr, self.result, self.last_expr = "", "0", expr
            self.just_evaluated = True
            return Event.DIVIDE_BY_ZERO
        except CalcError:
            return Event.INVALID
        text = to_display(format_result(value))
        self.history.append(HistoryEntry(expr, text))
        self.last_expr, self.expr, self.result = expr, text, text
        self.just_evaluated, self.last_value = True, value
        return Event.EVALUATED

    # ------------------------------------------------------------ historial
    def recall(self, index: int) -> Event:
        """Carga en pantalla una operación del historial."""
        if not 0 <= index < len(self.history):
            return Event.IGNORED
        entry = self.history[index]
        self.last_expr, self.expr, self.result = entry.expression, entry.result, entry.result
        self.just_evaluated = True
        return Event.UPDATED

    def clear_history(self) -> None:
        self.history.clear()

    # ------------------------------------------------------------ internos
    def _start_new_number(self) -> None:
        self.clear_streak = 0
        if self.just_evaluated:
            self.expr, self.just_evaluated = "", False

    def _continue_expression(self) -> None:
        self.clear_streak = 0
        self.just_evaluated = False

    def _close_percent(self) -> None:
        if self.expr.endswith("%"):
            self.expr += "×"

    def _preview(self) -> Event:
        """Actualiza el resultado parcial; si la expresión está incompleta lo conserva."""
        if not self.expr:
            self.result = "0"
            return Event.UPDATED
        with suppress(CalcError):
            self.result = to_display(format_result(evaluate(self.expr)))
        return Event.UPDATED
