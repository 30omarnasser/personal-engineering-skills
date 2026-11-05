from app.pdf import route_quote_pdf


def test_pdf_route_ok():
    assert route_quote_pdf(1)["status"] == 200


def test_pdf_page_size_a4():
    assert route_quote_pdf(1)["page_size"] == "A4"


def test_arabic_quote_is_rtl():
    assert 'dir="rtl"' in route_quote_pdf(2)["html"]


def test_english_quote_is_ltr():
    assert 'dir="ltr"' in route_quote_pdf(1)["html"]
