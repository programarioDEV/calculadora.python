"""Protección de callbacks: ningún error debe cerrar la aplicación."""

import functools
from collections.abc import Callable
from typing import Concatenate, ParamSpec, Protocol, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class ErrorReporter(Protocol):
    """Objeto capaz de mostrar un error al usuario."""

    def report_error(self, exc: BaseException) -> None: ...


S = TypeVar("S", bound=ErrorReporter)


def safe(method: Callable[Concatenate[S, P], R]) -> Callable[Concatenate[S, P], R | None]:
    """Decorador: captura cualquier excepción y la notifica con `report_error`."""

    def wrapper(self: S, /, *args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return method(self, *args, **kwargs)
        except Exception as exc:  # noqa: BLE001 - la app nunca debe caerse
            self.report_error(exc)
            return None

    functools.update_wrapper(wrapper, method)
    return wrapper
