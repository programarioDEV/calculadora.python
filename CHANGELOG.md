# Changelog

Todos los cambios relevantes de este proyecto se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto usa [versionado semántico](https://semver.org/lang/es/).

## [2.0.0] - 2026-10-10

### Añadido
- Paquete instalable con comando `dunder-calc` (layout `src/`, `pyproject.toml`).
- CI en GitHub Actions: ruff, mypy estricto, pytest con cobertura y construcción del paquete en Python 3.10–3.14.
- pre-commit, Dependabot, plantillas de issues y de pull request.
- 29 pruebas de motor, modelo, transformaciones, detectores y mapa de teclas.

### Cambiado
- Arquitectura dividida en `core/` (lógica pura) y `ui/` (tkinter), con módulos de 200 líneas como máximo.
- La ventana arranca con su tamaño natural, así que respeta el escalado de pantalla.

### Corregido
- El título, el subtítulo y los mensajes de estado ya no se recortan en pantallas con escalado.
- El panel de historial mantiene un ancho mínimo y no estrecha la calculadora.

## [1.0.0] - 2026-10-10

### Añadido
- Primera versión en un solo archivo: calculadora tkinter con ocho easter eggs.
