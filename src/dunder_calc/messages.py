"""Textos visibles de la aplicación (centralizados para editarlos o traducirlos)."""

APP_TITLE = "Dunder Mifflin Calculator"
NO_TKINTER = "tkinter no está disponible. En Debian/Ubuntu: sudo apt install python3-tk"

# Estado general
INPUT_FULL = "Límite de dígitos. Ni Oscar necesita tantos."
INVALID_EXPRESSION = "Operación incompleta o inválida."
DIVIDE_BY_ZERO_PLAIN = "No se puede dividir entre cero."
FLIP_PLAIN = "Pantalla volteada. Gira la cabeza."
UNEXPECTED_ERROR = "Algo falló ({name}), pero la oficina sigue abierta."
HISTORY_TITLE = "Historial de la sesión"
HISTORY_CLEAR = "Limpiar historial"
FLIP_BUTTON = "Voltear"
HISTORY_BUTTON = "Historial"

# Easter eggs
MICHAEL_ZERO_LINES: tuple[str, ...] = (
    "¿Dividir entre cero? Ni el Gerente Regional del Año se atreve a tanto.",
    "El cero no se reparte. Lo aprendí en un seminario carísimo.",
    "Eso no son matemáticas, es caos. Y el caos no está en el presupuesto.",
)
DIVIDE_BY_ZERO_RESULT = "¡Ni hablar!"

SCRANTON = "Scranton, PA · La Ciudad Eléctrica te saluda."

BONUS_WINDOW_TITLE = "Bono de fin de año"
BONUS_HEADING = "BONO DE FIN DE AÑO"
BONUS_BODY = (
    "¡Un millón! La gerencia te premia con:\n"
    "una taza de «Mejor Empleado» (casi sin usar)\n"
    "y un aplauso en la próxima junta."
)
BONUS_BUTTON = "Aceptar con humildad"
BONUS_STATUS = "Bono aprobado. Contabilidad aún no lo sabe."

FLIP_EGG = "Pantalla volteada… y revisada por Toby de RR.HH."

DWIGHT_BEET_FACTS: tuple[str, ...] = (
    "Una remolacha bien cuidada sobrevive a tres gerentes regionales.",
    "Los osos evitan el color remolacha. Lo comprobé personalmente.",
    "Nueve remolachas caben exactas en un maletín reglamentario.",
    "La remolacha no tiene sentido del humor. Por eso es superior.",
)

JELLO_ON = "Alguien metió tu grapadora en gelatina. Otra vez."
JELLO_OFF = "Grapadora rescatada. Todo vuelve a la normalidad."
MSPC_ON = "Michael Scott Paper Company: precios bajos, sueños enormes."
MSPC_OFF = "De vuelta en Dunder Mifflin. Nos compraron."

BANKRUPTCY_TEXT = "¡DECLARO BANCARROTA!"
BANKRUPTCY_STATUS = "Decirlo en voz alta no es un trámite legal. Pero se siente bien."
