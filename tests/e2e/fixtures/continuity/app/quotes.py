"""Quote model and totals (synthetic fixture)."""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Line:
    sku: str
    quantity: int
    unit_price: Decimal


@dataclass
class Quote:
    id: int
    customer: str
    lines: list[Line] = field(default_factory=list)
    language: str = "en"

    def total(self) -> Decimal:
        return sum((ln.unit_price * ln.quantity for ln in self.lines), Decimal("0"))


QUOTES: dict[int, Quote] = {
    1: Quote(1, "Example Contractor LLC", [Line("PX-200", 2, Decimal("1200.00"))]),
    2: Quote(2, "Example Utilities", [Line("VX-40", 5, Decimal("310.50"))], language="ar"),
}


def get_quote(quote_id: int) -> Quote:
    return QUOTES[quote_id]
