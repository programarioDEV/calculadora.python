"""Motor de cálculo: tokenizador y parser seguros (sin eval) sobre Decimal."""

import re
from decimal import Decimal, InvalidOperation, localcontext

from dunder_calc.config import MAX_EXPR_LEN

NUMBER_PATTERN = r"(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?"
_TOKEN_RE = re.compile(rf"\s*(?:({NUMBER_PATTERN})|(\S))")
_SYMBOLS = {"−": "-", "×": "*", "÷": "/"}
_VALID_SYMBOLS = frozenset("+-*/%()")


class CalcError(Exception):
    """Expresión inválida o error de cálculo."""


class DivisionByZeroError(CalcError):
    """Intento de división entre cero."""


def normalize(expr: str) -> str:
    """Convierte los símbolos de pantalla (−×÷) a operadores ASCII."""
    for symbol, ascii_op in _SYMBOLS.items():
        expr = expr.replace(symbol, ascii_op)
    return expr


def tokenize(expr: str) -> list[str]:
    """Divide la expresión en números, operadores, % y paréntesis."""
    tokens: list[str] = []
    for match in _TOKEN_RE.finditer(normalize(expr)):
        number, other = match.groups()
        if number:
            tokens.append(number)
        elif other in _VALID_SYMBOLS:
            tokens.append(other)
        elif other:
            raise CalcError(f"Carácter no válido: {other!r}")
    return tokens


class _Parser:
    """Parser descendente recursivo: expr → term → unary → postfix → primary."""

    def __init__(self, tokens: list[str]) -> None:
        self._tokens = tokens
        self._pos = 0

    def _peek(self) -> str | None:
        return self._tokens[self._pos] if self._pos < len(self._tokens) else None

    def _take(self) -> str | None:
        token = self._peek()
        self._pos += 1
        return token

    def parse(self) -> Decimal:
        if not self._tokens:
            raise CalcError("Expresión vacía")
        value = self._expr()
        if (extra := self._peek()) is not None:
            raise CalcError(f"Token inesperado: {extra}")
        return value

    def _expr(self) -> Decimal:
        value = self._term()
        while self._peek() in ("+", "-"):
            op = self._take()
            rhs = self._term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def _term(self) -> Decimal:
        value = self._unary()
        while self._peek() in ("*", "/"):
            op = self._take()
            rhs = self._unary()
            if op == "*":
                value *= rhs
            elif rhs == 0:
                raise DivisionByZeroError("División entre cero")
            else:
                value /= rhs
        return value

    def _unary(self) -> Decimal:
        if self._peek() in ("+", "-"):
            op = self._take()
            value = self._unary()
            return -value if op == "-" else value
        return self._postfix()

    def _postfix(self) -> Decimal:
        value = self._primary()
        while self._peek() == "%":
            self._take()
            value /= 100
        return value

    def _primary(self) -> Decimal:
        token = self._take()
        if token is None:
            raise CalcError("Expresión incompleta")
        if token == "(":
            value = self._expr()
            if self._take() != ")":
                raise CalcError("Falta ')'")
            return value
        if token[0].isdigit() or token[0] == ".":
            return Decimal(token)
        raise CalcError(f"Token inesperado: {token}")


def evaluate(expr: str) -> Decimal:
    """Evalúa una expresión aritmética de forma segura (sin eval)."""
    if not isinstance(expr, str):
        raise CalcError("La expresión debe ser texto")
    if len(expr) > MAX_EXPR_LEN:
        raise CalcError("Expresión demasiado larga")
    try:
        with localcontext() as ctx:
            ctx.prec = 28
            result = _Parser(tokenize(expr)).parse()
    except CalcError:
        raise
    except (InvalidOperation, ArithmeticError, RecursionError) as exc:
        raise CalcError(str(exc)) from exc
    if not result.is_finite():
        raise CalcError("Resultado no finito")
    return result


def format_result(value: Decimal, max_len: int = 16) -> str:
    """Formatea un Decimal para la pantalla (sin ceros sobrantes)."""
    if not value.is_finite():
        raise CalcError("Resultado no finito")
    with localcontext() as ctx:
        ctx.prec = 15
        value = +value
    if value == 0:
        return "0"
    if value == value.to_integral_value() and abs(value) < Decimal(10) ** max_len:
        return str(int(value))
    text = format(value.normalize(), "f")
    if len(text) > max_len:
        text = format(value.normalize(), ".10g")
    return text
