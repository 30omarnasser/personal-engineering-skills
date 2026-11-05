from app.pdf import route_quote_pdf


def test_arabic_font_embedded():
    # RTL font embedding is not implemented yet (pending work item).
    assert "@font-face" in route_quote_pdf(2)["html"]
