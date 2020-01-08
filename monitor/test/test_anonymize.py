import pytest

from mitmproxy import http
from tr069monitor import anonymize


@pytest.fixture
def request():
    return http.HTTPRequest.make(
        "GET", "http://acs.example.com/",
        """<soap:Body><cwmp:Inform>
            <Username>foo</Username>
            <Password>supersecret</Password>
        </cwmp:Inform></soap:Body>""",
        {"cookie": "supersecret", "SOAPAction": "Inform"}
    )


@pytest.fixture
def malformed_request():
    return http.HTTPRequest.make(
        "GET", "http://acs.example.com/",
        "malformed rpc with passwords"
    )


def test_anonymize(request):
    """If the message is parseable, we only want to retain the RPC command name and the URL"""
    anonymize.fully_anonymize(request)
    assert request.url == "http://acs.example.com/"
    assert "cookie" not in request.headers
    assert "SOAPAction" not in request.headers
    assert request.text == "<!-- redacted -->\n<soap:Body><cwmp:Inform/></soap:Body>"


def test_anonymize_malformed(malformed_request):
    """If the message is entirely unparseable, we do not want to keep anything."""
    anonymize.fully_anonymize(malformed_request)
    assert malformed_request.text == "<!-- redacted -->\n<soap:Body><None/></soap:Body>"


def test_redact(request):
    anonymize.redact(request)
    assert request.url == "http://acs.example.com/"
    assert "cookie" not in request.headers
    assert "supersecret" not in request.text
    assert "SOAPAction" in request.headers
    assert "<Username>foo</Username>" in request.text


def test_redact_malformed(malformed_request):
    anonymize.redact(malformed_request)
    assert malformed_request.text == "<!-- redacted -->\n<soap:Body><None/></soap:Body>"
