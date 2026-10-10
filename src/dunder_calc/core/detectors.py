"""Detectores de secuencias para easter eggs (sin dependencias de interfaz)."""

import time
from collections import deque
from collections.abc import Callable, Sequence


class SequenceDetector:
    """Detecta una secuencia exacta de teclas (p. ej. el código Konami)."""

    def __init__(self, sequence: Sequence[str]) -> None:
        self._sequence = tuple(item.lower() for item in sequence)
        self._buffer: deque[str] = deque(maxlen=len(self._sequence))

    def feed(self, item: str) -> bool:
        """Registra una tecla; devuelve True al completar la secuencia."""
        self._buffer.append(item.lower())
        if tuple(self._buffer) == self._sequence:
            self._buffer.clear()
            return True
        return False


class ClickCounter:
    """Cuenta clics consecutivos dentro de una ventana de tiempo."""

    def __init__(
        self, target: int, window_s: float, clock: Callable[[], float] = time.monotonic
    ) -> None:
        self._target = target
        self._window_s = window_s
        self._clock = clock
        self._count = 0
        self._last = float("-inf")

    def click(self) -> bool:
        """Registra un clic; devuelve True al alcanzar el objetivo."""
        now = self._clock()
        if now - self._last > self._window_s:
            self._count = 0
        self._count += 1
        self._last = now
        if self._count >= self._target:
            self._count = 0
            return True
        return False
