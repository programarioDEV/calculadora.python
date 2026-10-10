# Cómo contribuir

¡Gracias por tu interés! Las contribuciones son bienvenidas, sobre todo nuevos easter eggs.

## Preparar el entorno

```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e . --group dev
pre-commit install
```

## Antes de abrir un pull request

```bash
ruff check . && ruff format --check . && mypy && pytest
```

El CI ejecuta lo mismo en Python 3.10–3.14.

## Convenciones

- **Sin dependencias de ejecución**: solo la biblioteca estándar.
- **`core/` no importa tkinter.** Toda la lógica nueva va ahí, con pruebas en `tests/`.
- **Módulos de 200 líneas como máximo.** Si uno crece, divídelo por responsabilidad.
- **Type hints en todo** (mypy en modo estricto) y docstrings breves.
- **Textos visibles en `messages.py`**: frases cortas y originales, nada de citas largas de la serie.
- **Nuevos easter eggs**: un campo en `EasterEggSettings`, un método en `ui/eggs.py` y una fila en la tabla del README.
- Mensajes de commit en imperativo y concisos (p. ej. «Añade easter egg de Kevin y el chili»).
