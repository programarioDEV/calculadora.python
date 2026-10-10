"""Geometría de la ventana: cuadrícula, tamaño natural, panel lateral y escala."""

import tkinter as tk
from collections.abc import Callable

MIN_BASE_SIZE = (420, 640)
MIN_SCALE = 0.8
MAX_SCALE = 1.6
SIDE_PANEL_WIDTH = 280


class WindowLayout:
    """Coloca los widgets en la cuadrícula y adapta la ventana a su contenido."""

    def __init__(
        self,
        root: tk.Tk,
        header: tk.Widget,
        display: tk.Widget,
        keypad: tk.Widget,
        side_panel: tk.Widget,
        on_scale: Callable[[float], None],
    ) -> None:
        self._root = root
        self._side_panel = side_panel
        self._on_scale = on_scale
        self._base_size = MIN_BASE_SIZE
        self._panel_visible = False
        self._panel_grew_window = False

        root.columnconfigure(0, weight=1, minsize=300)
        root.rowconfigure(2, weight=1)
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 6))
        display.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 8))
        keypad.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        side_panel.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=(0, 12), pady=12)
        side_panel.grid_remove()
        root.bind("<Configure>", self._on_configure)

    def fit_to_content(self) -> None:
        """Usa el tamaño natural de la ventana, que respeta el escalado de pantalla."""
        self._root.update_idletasks()
        width = max(MIN_BASE_SIZE[0], self._root.winfo_reqwidth())
        height = max(MIN_BASE_SIZE[1], self._root.winfo_reqheight())
        self._base_size = (width, height)
        self._root.geometry(f"{width}x{height}")
        self._root.minsize(int(width * MIN_SCALE), int(height * MIN_SCALE))

    def toggle_side_panel(self) -> None:
        """Muestra u oculta el panel lateral, ensanchando la ventana si hace falta."""
        self._panel_visible = not self._panel_visible
        width, height = self._root.winfo_width(), self._root.winfo_height()
        if self._panel_visible:
            self._root.columnconfigure(1, minsize=SIDE_PANEL_WIDTH)
            self._side_panel.grid()
            if width < self._base_size[0] + SIDE_PANEL_WIDTH:
                self._root.geometry(f"{width + SIDE_PANEL_WIDTH}x{height}")
                self._panel_grew_window = True
            return
        self._side_panel.grid_remove()
        self._root.columnconfigure(1, minsize=0)
        if self._panel_grew_window:
            self._root.geometry(f"{width - SIDE_PANEL_WIDTH}x{height}")
            self._panel_grew_window = False

    def _on_configure(self, event: tk.Event) -> None:
        if event.widget is not self._root:
            return
        main_width = event.width - (SIDE_PANEL_WIDTH if self._panel_visible else 0)
        ratio = min(main_width / self._base_size[0], event.height / self._base_size[1])
        self._on_scale(max(MIN_SCALE, min(MAX_SCALE, ratio)))
