import os

from tr069 import proxy


def test_proxy():
    proxy.enable("http://example.com:8080/")
    assert "HTTP_PROXY" in os.environ
    assert "REQUESTS_CA_BUNDLE" not in os.environ

    proxy.enable("http://example.com:8080/", "foo")
    assert "HTTP_PROXY" in os.environ
    assert "REQUESTS_CA_BUNDLE" in os.environ

    proxy.disable()
    assert "HTTP_PROXY" not in os.environ
    assert "REQUESTS_CA_BUNDLE" not in os.environ
