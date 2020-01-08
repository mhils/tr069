import textwrap

from click.testing import CliRunner

import tr069
from tr069.__main__ import cli


def test_main():
    result = CliRunner().invoke(
        cli,
        args=["http://acs.example.com/", "--no-server"],
        input=textwrap.dedent("""
            84 / 2
            x = 1
            invalid
            exit()
        """)
    )
    assert "42.0" in result.output
    assert "NameError: name 'invalid' is not defined" in result.output
    assert isinstance(result.exception, SystemExit)


def test_connection_request_server(monkeypatch):
    monkeypatch.setattr(tr069, "ConnectionRequestServer", lambda: print("<server started>"))
    result = CliRunner().invoke(
        cli,
        args=["http://acs.example.com/", "--server"],
        input="exit()"
    )
    assert "<server started>" in result.output


def test_auth():
    result = CliRunner().invoke(
        cli,
        args=["http://acs.example.com/", "--basic-auth", "user", "pass"],
        input="exit()"
    )
    assert 'basic_auth=("user", "pass")' in result.output

    result = CliRunner().invoke(
        cli,
        args=["http://acs.example.com/", "-d", "user", "pass"],
        input="exit()"
    )
    assert 'digest_auth=("user", "pass")' in result.output
