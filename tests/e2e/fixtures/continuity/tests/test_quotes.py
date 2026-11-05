from decimal import Decimal

import pytest

from app.quotes import Line, Quote, get_quote


def test_total_single_line():
    assert get_quote(1).total() == Decimal("2400.00")


def test_total_multiple_lines():
    q = Quote(9, "c", [Line("a", 1, Decimal("1.50")), Line("b", 2, Decimal("2.25"))])
    assert q.total() == Decimal("6.00")


def test_empty_quote_total_is_zero():
    assert Quote(10, "c").total() == Decimal("0")


def test_arabic_quote_language():
    assert get_quote(2).language == "ar"


def test_unknown_quote_raises():
    with pytest.raises(KeyError):
        get_quote(404)
