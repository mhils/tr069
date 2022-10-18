import warnings

import requests
import requests.auth
from typing import List, Tuple, Any, Dict, Union, Optional

from tr069 import util
from tr069.data import device as mdevice
from tr069.data import rpcs
from tr069.data import soap


def _wrap_rpc(rpc):
    """
    Copy documentation and annotations from RPC function
    so that they are available from help(Client)
    """

    def decorator(fn):
        fn.__doc__ = rpc.__doc__
        fn.__annotations__ = rpc.__annotations__.copy()
        fn.__annotations__["return"] = requests.Response
        return fn

    return decorator


class Client:
    """A TR-069 Client instance to interact with an ACS."""

    acs_url: str
    requests_kwargs: Dict[str, Any]
    device: mdevice.Device
    log: bool
    _session: requests.Session
    messages: List[requests.Response]

    def __init__(
            self,
            acs_url: str,
            device: mdevice.Device = mdevice.DEFAULT,
            *,
            log: bool = True,
            basic_auth: Optional[Tuple[str, str]] = None,
            digest_auth: Optional[Tuple[str, str]] = None,
            cert: Union[Tuple[str, str], str] = None,
            **requests_kwargs
    ):
        """
        Args:
            acs_url: The ACS URL.
            device: The device represented by the client.
            log: If True, all requests and responses are logged to stdout.
            basic_auth: A (user, pass) tuple used for HTTP basic authentication.
            digest_auth: A (user, pass) tuple used for HTTP digest authentication.
            cert: TLS Client Certificate, see http://docs.python-requests.org/en/master/user/advanced/#ssl-cert-verification
            **requests_kwargs: Additional arguments passed to subsequent internal calls of requests.post().
        """
        self.acs_url = acs_url
        self.device = device
        self.log = log

        # auth and cert are actually just added explicitly to improve the documentation.
        if [basic_auth, digest_auth, requests_kwargs.get("auth", None)].count(None) < 2:
            raise ValueError(
                "auth, basic_auth and digest_auth authentication are mutually exclusive.")
        if basic_auth:
            requests_kwargs["auth"] = requests.auth.HTTPBasicAuth(*basic_auth)
        if digest_auth:
            requests_kwargs["auth"] = requests.auth.HTTPDigestAuth(*digest_auth)

        if cert:
            requests_kwargs["cert"] = cert
        self.requests_kwargs = requests_kwargs
        self._session = requests.Session()
        self.messages = []

    @staticmethod
    def _default_headers(data: str):
        default_headers = {
            "User-Agent": None,
        }

        # TR-069 3.4.1: An empty HTTP POST MUST NOT contain a Content-Type header
        if data:
            default_headers["Content-Type"] = 'text/xml; charset="utf-8"'

        # Add proper SOAPAction header (TR-069 3.4.1)
        soap_action = soap.extract_rpc_name(data)
        if soap_action:
            if "Response" in soap_action:
                # Add empty header.
                default_headers["SOAPAction"] = ""
            else:
                default_headers["SOAPAction"] = soap_action

        return default_headers

    def request(self, data: str, *, fix_cwmp_id: bool = True, **kwargs) -> requests.Response:
        """
        Send a HTTP request to the ACS.

        Args:
            data: The request body
            fix_cwmp_id: If true, the cwmp:ID in the body will replaced with the cwmp:ID in the last response.
            **kwargs: Arguments passed to self._session.post()

        Returns:
            The ACS' response.
        """
        kwargs.update(self.requests_kwargs)
        kwargs.setdefault("headers", self._default_headers(data))

        # Re-use the cwmp:ID transmitted in the last response.
        # For client RPCs, that's going to be our default id, so nothing should be changed.
        # For server RPCs, that's the id sent by the server, which we need to account for.
        if fix_cwmp_id and self.messages:
            data = soap.fix_cwmp_id(data, self.messages[-1].text)

        resp = self._session.post(self.acs_url, data=data, **kwargs)
        self._record_response(resp)
        return resp

    def replay(self, request: Optional[requests.PreparedRequest] = None) -> requests.Response:
        """
        Replay a request that has previously been sent.
        Useful to e.g. test for nonce re-use.

        Args:
            request: The request to replay. If no request is passed, the last request
                     will be replayed.
        """
        if request is None:
            request = self.messages[-1].request.copy()

        resp = self._session.send(request)
        self._record_response(resp)
        return resp

    def _record_response(self, response: requests.Response) -> None:
        self.messages.append(response)
        if self.log:
            # don't log request before sending it, requests adds its own headers after that.
            util.print_http_flow(response)

    def __repr__(self) -> str:
        return f"tr069.Client({self.acs_url}, {len(self.messages)} messages)"

    def done(self) -> requests.Response:
        """Indicate to the ACS that the client has finished sending RPCs"""
        return self.request("")

    def handle_server_rpcs(self) -> int:
        """
        Handle server RPCs automatically, starting with the last already transmitted RPC.
        This is usually called immediately after .done()

        Returns:
            The number of handled RPCs

        Raises:
            NotImplementedError if automated handling of the RPC is not implemented.
        """
        count = 0
        while True:
            rpc = self.messages[-1]
            if rpc.status_code == 204:
                break
            self._handle_server_rpc(rpc)
            count += 1
        return count

    def _handle_server_rpc(self, rpc: requests.Response):
        rpc_name = soap.extract_rpc_name(rpc.text) or "unknown"
        if rpc_name == "cwmp:SetParameterValues":
            new_params = rpcs.parse_set_parameter_values(rpc.text)
            self.device.params.update({p.name: p for p in new_params})
            self.set_parameter_values_response()
        elif rpc_name == "cwmp:GetParameterValues":
            param_names = rpcs.parse_get_parameter_values(rpc.text)
            params = []
            for p in param_names:
                params.extend(self.device.params.all(p))
            self.get_parameter_values_response(params)
        elif rpc_name == "cwmp:SetParameterAttributes":
            warnings.warn("Ignoring cwmp:SetParameterAttributes")
            self.set_parameter_attributes_response()
        elif rpc_name == "cwmp:GetParameterNames":
            # We ignore next_level because no-one validates that anyways.
            path, _ = rpcs.parse_get_parameter_names(rpc.text)
            params = self.device.params.all(path)
            self.get_parameter_names_response(params)
        elif rpc_name == "cwmp:Download":
            self.download_response()
        else:
            raise NotImplementedError(f"Unknown server RPC: {rpc_name}")

    def close(self) -> None:
        """
        Close any existing connections to the ACS and reset the session.
        """
        self._session.close()
        self._session = requests.Session()
        if self.log:
            print("Connection closed.")

    @_wrap_rpc(rpcs.make_inform)
    def inform(self, **kwargs):
        kwargs.setdefault("device", self.device)
        return self.request(rpcs.make_inform(**kwargs))

    @_wrap_rpc(rpcs.make_get_rpc_methods)
    def get_rpc_methods(self) -> requests.Response:
        return self.request(rpcs.make_get_rpc_methods())

    @_wrap_rpc(rpcs.make_request_download)
    def request_download(self, *args, **kwargs):
        return self.request(rpcs.make_request_download(*args, **kwargs))

    @_wrap_rpc(rpcs.make_set_parameter_values_response)
    def set_parameter_values_response(self, *args, **kwargs):
        return self.request(rpcs.make_set_parameter_values_response(*args, **kwargs))

    @_wrap_rpc(rpcs.make_get_parameter_values_response)
    def get_parameter_values_response(self, *args, **kwargs):
        return self.request(rpcs.make_get_parameter_values_response(*args, **kwargs))

    @_wrap_rpc(rpcs.make_set_parameter_attributes_response)
    def set_parameter_attributes_response(self):
        return self.request(rpcs.make_set_parameter_attributes_response())

    @_wrap_rpc(rpcs.make_get_parameter_names_response)
    def get_parameter_names_response(self, *args, **kwargs):
        return self.request(rpcs.make_get_parameter_names_response(*args, **kwargs))

    @_wrap_rpc(rpcs.make_download_response)
    def download_response(self, *args, **kwargs):
        return self.request(rpcs.make_download_response(*args, **kwargs))
