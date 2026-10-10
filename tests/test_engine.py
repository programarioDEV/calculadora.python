"""Pruebas del motor de cálculo."""

import unittest
from decimal import Decimal

from dunder_calc.core.engine import CalcError, DivisionByZeroError, evaluate, format_result


class TestEngine(unittest.TestCase):
    def test_precedence(self) -> None:
        self.assertEqual(evaluate("2+3×4−5÷5"), Decimal(13))

    def test_decimals_are_exact(self) -> None:
        self.assertEqual(format_result(evaluate("0.1+0.2")), "0.3")
        self.assertEqual(format_result(evaluate("1÷3")), "0.3333333333")

    def test_division_by_zero(self) -> None:
        with self.assertRaises(DivisionByZeroError):
            evaluate("7÷0")

    def test_unary_minus_and_percent(self) -> None:
        self.assertEqual(evaluate("5×−3"), Decimal(-15))
        self.assertEqual(evaluate("200×10%"), Decimal(20))

    def test_invalid_input(self) -> None:
        for bad in ("", "5+", "2××3", "import os", "1.2.3", "9" * 300):
            with self.subTest(bad=bad[:20]), self.assertRaises(CalcError):
                evaluate(bad)

    def test_format_large_and_small(self) -> None:
        self.assertEqual(format_result(evaluate("99999999×99999999×99999999")), "9.9999997e+23")
        self.assertEqual(format_result(evaluate("0−10")), "-10")


if __name__ == "__main__":
    unittest.main()
