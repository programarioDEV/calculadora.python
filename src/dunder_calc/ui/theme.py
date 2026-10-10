"""Paletas de color de la interfaz."""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


class ButtonKind(str, Enum):
    """Familias de botones con colores propios."""

    NUM = "num"
    OP = "op"
    FN = "fn"
    EQ = "eq"


@dataclass(frozen=True, slots=True)
class ButtonColors:
    bg: str
    fg: str
    hover: str


@dataclass(frozen=True)
class Theme:
    """Paleta completa de un tema."""

    name: str
    subtitle: str
    bg: str
    panel: str
    display_bg: str
    display_fg: str
    display_sub: str
    title_fg: str
    subtitle_fg: str
    accent: str
    accent_fg: str
    buttons: Mapping[ButtonKind, ButtonColors]

    def button(self, kind: ButtonKind) -> ButtonColors:
        return self.buttons[kind]


def _buttons(
    num: tuple[str, str, str],
    op: tuple[str, str, str],
    fn: tuple[str, str, str],
    eq: tuple[str, str, str],
) -> dict[ButtonKind, ButtonColors]:
    """Atajo para declarar (fondo, texto, hover) de cada familia de botones."""
    return {
        ButtonKind.NUM: ButtonColors(*num),
        ButtonKind.OP: ButtonColors(*op),
        ButtonKind.FN: ButtonColors(*fn),
        ButtonKind.EQ: ButtonColors(*eq),
    }


DEFAULT_THEME = "dunder"

THEMES: dict[str, Theme] = {
    "dunder": Theme(
        name="dunder",
        subtitle="Sucursal Scranton · Papel y cálculos de calidad",
        bg="#F5F1E6",
        panel="#FFFFFF",
        display_bg="#1F3A5F",
        display_fg="#F5F1E6",
        display_sub="#A9C0DA",
        title_fg="#1F3A5F",
        subtitle_fg="#5A6B7F",
        accent="#F2B134",
        accent_fg="#1F2A36",
        buttons=_buttons(
            num=("#FFFFFF", "#1F2A36", "#E3EAF3"),
            op=("#2E5D8E", "#FFFFFF", "#3C74AD"),
            fn=("#D9DEE5", "#1F2A36", "#C2CBD7"),
            eq=("#F2B134", "#1F2A36", "#F6C561"),
        ),
    ),
    "jello": Theme(
        name="jello",
        subtitle="Departamento de Gelatina · Grapadora no disponible",
        bg="#F1FAE3",
        panel="#FFFFFF",
        display_bg="#2F6B1F",
        display_fg="#F4FFE8",
        display_sub="#BFE6A0",
        title_fg="#2F6B1F",
        subtitle_fg="#5E8F3C",
        accent="#FFE066",
        accent_fg="#24420F",
        buttons=_buttons(
            num=("#FFFFFF", "#24420F", "#E2F4CF"),
            op=("#8CCB4E", "#1B330A", "#A5DA70"),
            fn=("#FFF1A8", "#5A4A00", "#FFE77A"),
            eq=("#4E9A22", "#FFFFFF", "#62B232"),
        ),
    ),
    "mspc": Theme(
        name="mspc",
        subtitle="Michael Scott Paper Company · Desde un armario",
        bg="#EADBC8",
        panel="#F7EFE3",
        display_bg="#5B3A29",
        display_fg="#F7EFE3",
        display_sub="#D8BFA6",
        title_fg="#8B1E1E",
        subtitle_fg="#6B4F3A",
        accent="#E4B363",
        accent_fg="#3B2A1E",
        buttons=_buttons(
            num=("#F7EFE3", "#3B2A1E", "#EADAC4"),
            op=("#8B5E3C", "#FFFFFF", "#A06F49"),
            fn=("#D4BFA3", "#3B2A1E", "#C4AC8C"),
            eq=("#B22222", "#FFFFFF", "#C83A3A"),
        ),
    ),
}


def get_theme(name: str) -> Theme:
    """Tema por nombre; recurre al tema por defecto si no existe."""
    return THEMES.get(name, THEMES[DEFAULT_THEME])
