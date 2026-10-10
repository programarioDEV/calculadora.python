"""Pruebas de transformaciones, detectores y mapa de teclas."""

import unittest
from decimal import Decimal

from dunder_calc.config import KONAMI_CODE, EasterEggSettings
from dunder_calc.core.detectors import ClickCounter, SequenceDetector
from dunder_calc.core.keymap import Action, Command, map_key
from dunder_calc.core.transforms import (
    SFW_FLIP,
    flip_display,
    is_flip_egg,
    result_easter_egg,
    toggle_sign,
)


class TestTransforms(unittest.TestCase):
    def test_toggle_sign(self) -> None:
        cases = {"12": "−12", "−12": "12", "5×−3": "5×3", "5+3": "5−3", "5−3": "5+3"}
        for before, after in cases.items():
            with self.subTest(before=before):
                self.assertEqual(toggle_sign(before), after)

    def test_flip_is_work_appropriate(self) -> None:
        self.assertEqual(flip_display("5318008"), SFW_FLIP)
        self.assertEqual(flip_display("0.7734"), "hELL.O")
        self.assertTrue(is_flip_egg("5318008"))

    def test_result_eggs_respect_settings(self) -> None:
        self.assertEqual(result_easter_egg(Decimal(570)), "scranton")
        self.assertEqual(result_easter_egg(Decimal("9.0")), "beet_fact")
        self.assertIsNone(result_easter_egg(Decimal(570), EasterEggSettings(scranton=False)))


class TestDetectors(unittest.TestCase):
    def test_konami(self) -> None:
        detector = SequenceDetector(KONAMI_CODE)
        keys = ["Up", "Up", "Down", "Down", "Left", "Right", "Left", "Right", "B", "a"]
        self.assertEqual([detector.feed(k) for k in keys][-1], True)
        self.assertFalse(detector.feed("Up"))

    def test_click_counter_window(self) -> None:
        now = [0.0]
        counter = ClickCounter(target=3, window_s=1.0, clock=lambda: now[0])
        self.assertFalse(counter.click())
        now[0] = 5.0  # Pasó demasiado tiempo: se reinicia.
        self.assertFalse(counter.click())
        self.assertFalse(counter.click())
        self.assertTrue(counter.click())


class TestKeymap(unittest.TestCase):
    def test_map_key(self) -> None:
        self.assertEqual(map_key("7", "7"), Command(Action.DIGIT, "7"))
        self.assertEqual(map_key("-", "minus"), Command(Action.OPERATOR, "−"))
        self.assertEqual(map_key("\r", "Return"), Command(Action.EQUALS))
        self.assertEqual(map_key("\x1b", "Escape"), Command(Action.CLEAR))
        self.assertIsNone(map_key("", "Up"))


if __name__ == "__main__":
    unittest.main()
