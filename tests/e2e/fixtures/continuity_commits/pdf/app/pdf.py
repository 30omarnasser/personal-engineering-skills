"""PDF export for quotes (synthetic fixture; rendering is stubbed, see ADR-0007)."""
from __future__ import annotations

from app.quotes import get_quote

PAGE_SIZE = "A4"


def render_html(quote_id: int) -> str:
    q = get_quote(quote_id)
    direction = "rtl" if q.language == "ar" else "ltr"
    rows = "".join(f"<tr><td>{ln.sku}</td><td>{ln.quantity}</td><td>{ln.unit_price}</td></tr>" for ln in q.lines)
    return (f'<html dir="{direction}"><body><h1>Quote {q.id}</h1><p>{q.customer}</p>'
            f"<table>{rows}</table><p>Total: {q.total()}</p></body></html>")


def route_quote_pdf(quote_id: int) -> dict:
    """GET /quotes/{id}/pdf — returns the HTML that WeasyPrint will render."""
    return {"status": 200, "page_size": PAGE_SIZE, "html": render_html(quote_id)}
