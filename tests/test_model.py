"""Pruebas del modelo de edición (sin interfaz)."""

import unittest
from decimal import Decimal

from dunder_calc.config import CLEAR_STREAK_TARGET
from dunder_calc.core.keymap import map_button
from dunder_calc.core.model import CalculatorModel, Event


def press(model: CalculatorModel, keys: str) -> Event:
    """Pulsa una secuencia de botones y devuelve el último evento."""
    event = Event.IGNORED
    for label in keys:
        event = model.apply(map_button(label))
    return event


class TestCalculatorModel(unittest.TestCase):
    def setUp(self) -> None:
        self.model = CalculatorModel()

    def test_evaluates_and_records_history(self) -> None:
        self.assertIs(press(self.model, "12+3×2="), Event.EVALUATED)
        self.assertEqual(self.model.result, "18")
        self.assertEqual(str(self.model.history[-1]), "12+3×2 = 18")
        self.assertEqual(self.model.last_value, Decimal(18))

    def test_live_preview_keeps_last_valid_result(self) -> None:
        press(self.model, "8×")
        self.assertEqual(self.model.result, "8")

    def test_operator_after_result_chains(self) -> None:
        press(self.model, "2+2=+1=")
        self.assertEqual(self.model.result, "5")

    def test_digit_after_result_starts_over(self) -> None:
        press(self.model, "2+2=7")
        self.assertEqual(self.model.expr, "7")

    def test_operator_replaces_previous_operator(self) -> None:
        press(self.model, "5+×")
        self.assertEqual(self.model.expr, "5×")

    def test_leading_zero_and_double_dot(self) -> None:
        press(self.model, "007..5")
        self.assertEqual(self.model.expr, "7.5")

    def test_toggle_sign(self) -> None:
        press(self.model, "5−3±")
        self.assertEqual(self.model.expr, "5+3")

    def test_divide_by_zero_event(self) -> None:
        self.assertIs(press(self.model, "5÷0="), Event.DIVIDE_BY_ZERO)
        self.assertEqual(self.model.expression_line, "5÷0 =")

    def test_invalid_equals(self) -> None:
        self.assertIs(press(self.model, "5×="), Event.INVALID)

    def test_clear_streak(self) -> None:
        events = [press(self.model, "C") for _ in range(CLEAR_STREAK_TARGET)]
        self.assertIs(events[-1], Event.CLEAR_STREAK)
        self.assertNotIn(Event.CLEAR_STREAK, events[:-1])

    def test_other_key_breaks_clear_streak(self) -> None:
        press(self.model, "C" * (CLEAR_STREAK_TARGET - 1) + "1")
        self.assertIs(press(self.model, "C"), Event.UPDATED)

    def test_recall_history(self) -> None:
        press(self.model, "4×4=C")
        self.assertIs(self.model.recall(0), Event.UPDATED)
        self.assertEqual(self.model.result, "16")
        self.assertIs(self.model.recall(5), Event.IGNORED)


if __name__ == "__main__":
    unittest.main()
