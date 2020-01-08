import io
import socket

import click
import requests

try:
    from mitmproxy.contentviews import xml_html
except ImportError:  # pragma: no cover
    xml_html = None

try:
    import pygments
except ImportError:  # pragma: no cover
    pygments = None
else:
    import pygments.lexers
    import pygments.formatters


def format_xml_if_available(xml: str) -> str:
    """
    Formats the xml if the XML formatter is installed,
    returns it unmodified otherwise
    """
    if not xml_html:
        return xml
    tokens = xml_html.tokenize(xml)
    return xml_html.format_xml(tokens)


def highlight_if_available(
        message: str,
        lexer: str = "http",
        formatter: str = "console"
) -> str:
    """
    Highlights the message if pygments is installed,
    returns it unmodified otherwise
    """

    if not pygments:
        return message
    return pygments.highlight(
        message,
        pygments.lexers.get_lexer_by_name(lexer),
        pygments.formatters.get_formatter_by_name(formatter)
    )


def print_http_flow(
        resp: requests.Response,
) -> None:
    """
    Print an HTTP flow in the nicest way possible.
    """
    req = resp.request
    request = io.StringIO()
    request.write(f"{req.method} {req.path_url} HTTP/1.1\r\n")
    for name, value in req.headers.items():
        request.write(f"{name}: {value}\r\n")
    request.write("\r\n")
    request.write(format_xml_if_available(req.body or ""))

    response = io.StringIO()
    response.write(f"HTTP/1.1 {resp.status_code} {resp.reason}\r\n")
    for name, value in resp.headers.items():
        response.write(f"{name}: {value}\r\n")
    response.write("\r\n")
    response.write(format_xml_if_available(resp.text))

    click.secho(">> Request\r\n", fg="green", bold=True)
    click.echo(highlight_if_available(request.getvalue()))
    click.secho("<< Response\r\n", fg="red", bold=True)
    click.echo(highlight_if_available(response.getvalue()))


def get_ip() -> str:
    """
    Gets the machine's primary outgoing IP
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    return s.getsockname()[0]
