import textwrap

from hypothesis import example
from hypothesis import given
from hypothesis.strategies import text

from tr069 import util


@given(text())
@example('<xml>test <a foo="bar"/></xml>')
@example('<xml</xml>')
def test_format_xml(monkeypatch, s):
    assert isinstance(util.format_xml_if_available(s), str)
    monkeypatch.setattr(util, "xml_html", None)
    assert util.format_xml_if_available(s) == s


@given(text())
@example('<xml>test <a foo="bar"/></xml>')
@example('<xml</xml>')
def test_highlight(monkeypatch, s):
    assert isinstance(util.highlight_if_available(s, "xml"), str)
    monkeypatch.setattr(util, "pygments", None)
    assert util.highlight_if_available(s) == s


def test_print_http_flow(capsys, response):
    util.print_http_flow(response)

    out = capsys.readouterr()[0].strip().replace("\r\n", "\n")
    assert out == textwrap.dedent("""
        >> Request

        POST / HTTP/1.1
        foo: bar
        Content-Length: 3

        qux

        << Response

        HTTP/1.1 200 OK
        bar: baz

        quux
    """).strip()


def test_get_ip():
    assert util.get_ip()
