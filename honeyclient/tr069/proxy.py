import os
from typing import Optional


def enable(url: str, ca_certs: Optional[str] = None) -> None:
    """
    Route all outgoing requests through a proxy.

    Args:
        url: The proxy URL.
        ca_certs: path to a certificate list stored in PEM format (optional).

    """
    os.environ.update({
        "HTTP_PROXY": url,
        "HTTPS_PROXY": url,
    })
    if ca_certs:
        os.environ["REQUESTS_CA_BUNDLE"] = ca_certs
    else:
        os.environ.pop("REQUESTS_CA_BUNDLE", None)


def disable() -> None:
    """
    Disable proxying of requests.
    """
    for var in ["HTTP_PROXY", "HTTPS_PROXY", "REQUESTS_CA_BUNDLE"]:
        os.environ.pop(var, None)
