"""Controlador principal: conecta el modelo, los widgets y los easter eggs."""

import tkinter as tk
from contextlib import suppress
from types import TracebackType

from dunder_calc import messages
from dunder_calc.config import (
    EASTER_EGGS,
    KONAMI_CODE,
    TITLE_CLICKS_TARGET,
    TITLE_CLICKS_WINDOW_S,
    EasterEggSettings,
)
from dunder_calc.core.detectors import ClickCounter, SequenceDetector
from dunder_calc.core.keymap import Action, Command, map_key
from dunder_calc.core.model import CalculatorModel, Event
from dunder_calc.core.transforms import flip_display, result_easter_egg
from dunder_calc.ui.animator import Animator
from dunder_calc.ui.eggs import EasterEggs
from dunder_calc.ui.fonts import FontSet
from dunder_calc.ui.panels import HistoryPanel, Keypad
from dunder_calc.ui.safety import safe
from dunder_calc.ui.theme import DEFAULT_THEME, Theme, get_theme
from dunder_calc.ui.widgets import Display, Header
from dunder_calc.ui.window import WindowLayout


class CalculatorApp:
    """Ventana de la calculadora Dunder Mifflin."""

    def __init__(
        self,
        root: tk.Tk,
        model: CalculatorModel | None = None,
        settings: EasterEggSettings = EASTER_EGGS,
    ) -> None:
        self.root = root
        self.model = model or CalculatorModel()
        self.settings = settings
        self._theme = get_theme(DEFAULT_THEME)
        self._konami = SequenceDetector(KONAMI_CODE)
        self._title_clicks = ClickCounter(TITLE_CLICKS_TARGET, TITLE_CLICKS_WINDOW_S)

        root.title(messages.APP_TITLE)
        self.fonts = FontSet(root)
        self.header = Header(root, self.fonts, on_title_click=self.on_title_click)
        self.display = Display(root, self.fonts)
        self.keypad = Keypad(root, self.fonts, on_command=self.execute)
        self.history = HistoryPanel(
            root, self.fonts, on_pick=self.recall_history, on_clear=self.clear_history
        )
        self.layout = WindowLayout(
            root, self.header, self.display, self.keypad, self.history, on_scale=self._on_scale
        )

        self.animator = Animator(root, on_cancel=lambda: self.display.paint(self._theme))
        self.eggs = EasterEggs(root, self, self.display, self.animator, self.fonts, settings)

        root.report_callback_exception = self._on_tk_error
        root.bind("<Key>", self.on_key)
        self.apply_theme(DEFAULT_THEME)
        self.render()
        self.layout.fit_to_content()

    # ------------------------------------------------------------ tema y vista
    @property
    def theme(self) -> Theme:
        return self._theme

    def apply_theme(self, name: str) -> None:
        """Aplica una paleta a todos los widgets."""
        self._theme = theme = get_theme(name)
        self.root.configure(bg=theme.bg)
        for widget in (self.header, self.keypad, self.history):
            widget.apply_theme(theme)
        self.display.paint(theme)

    def render(self) -> None:
        self.display.show(self.model.expression_line, self.model.result)

    def report_error(self, exc: BaseException) -> None:
        with suppress(tk.TclError):
            self.display.set_status(messages.UNEXPECTED_ERROR.format(name=type(exc).__name__))

    # ------------------------------------------------------------ comandos
    @safe
    def execute(self, command: Command) -> None:
        """Punto único de entrada para botones y teclado."""
        self.animator.cancel_all()
        self.display.set_status("")
        if command.action is Action.FLIP:
            self._flip()
        elif command.action is Action.HISTORY:
            self.toggle_history()
        else:
            event = self.model.apply(command)
            self.render()
            self._handle(event)

    def _handle(self, event: Event) -> None:
        match event:
            case Event.INPUT_FULL:
                self.display.set_status(messages.INPUT_FULL)
            case Event.INVALID:
                self.display.set_status(messages.INVALID_EXPRESSION)
            case Event.DIVIDE_BY_ZERO:
                if not self.eggs.divide_by_zero():
                    self.display.set_result("Error")
                    self.display.set_status(messages.DIVIDE_BY_ZERO_PLAIN)
            case Event.EVALUATED:
                self.history.add(str(self.model.history[-1]))
                self._check_result_eggs()
            case Event.CLEAR_STREAK:
                self.eggs.bankruptcy()
            case _:
                pass

    def _check_result_eggs(self) -> None:
        value = self.model.last_value
        name = result_easter_egg(value, self.settings) if value is not None else None
        if name and (egg := self.eggs.by_name(name)):
            egg()

    def _flip(self) -> None:
        shown = self.model.result
        if not self.eggs.flip(shown):
            self.display.set_result(flip_display(shown))
            self.display.set_status(messages.FLIP_PLAIN)

    # ------------------------------------------------------------ historial
    @safe
    def toggle_history(self) -> None:
        self.layout.toggle_side_panel()

    @safe
    def recall_history(self, index: int) -> None:
        self.animator.cancel_all()
        self.display.set_status("")
        self.model.recall(index)
        self.render()

    @safe
    def clear_history(self) -> None:
        self.model.clear_history()
        self.history.clear()

    # ------------------------------------------------------------ eventos de Tk
    @safe
    def on_key(self, event: tk.Event) -> None:
        """Atajos de teclado y detector del código Konami."""
        if self._konami.feed(event.keysym):
            self.eggs.konami()
        if command := map_key(event.char, event.keysym):
            self.execute(command)

    @safe
    def on_title_click(self) -> None:
        if self._title_clicks.click():
            self.eggs.jello()

    def _on_scale(self, scale: float) -> None:
        if self.fonts.rescale(scale):
            self.display.refit()
            self.header.refit()

    def _on_tk_error(
        self, _exc_type: type[BaseException], exc: BaseException, _tb: TracebackType | None
    ) -> None:
        self.report_error(exc)
