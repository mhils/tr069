import textwrap
from typing import Hashable, List, MutableMapping

from mitmproxy import flowfilter
from mitmproxy import http
from mitmproxy.net.http import Message
from tr069.data import soap


class RPC:
    """A single remote procedure call, either issued by client or server."""
    command: Message
    response: Message

    def __init__(self, command):
        self._check(command)
        self.command = command
        self.response = None

    def _check(self, message: Message):
        if not message.text:
            raise ValueError(f"Empty RPC: {message}")
        if not soap.extract_rpc_name(message.text):
            raise ValueError(f"Invalid RPC: {message}")

    @property
    def from_client(self):
        return isinstance(self.command, http.HTTPRequest)

    def add_response(self, resp):
        self._check(resp)
        if self.response is not None:
            raise RuntimeError("RPC already has a response")
        self.response = resp

    def __repr__(self):
        command = soap.extract_rpc_name(self.command.text)
        resp = soap.extract_rpc_name(self.response.text)
        return f"{'>>' if self.from_client else '<<'} {command} -> {resp}"


class Session:
    """A session consisting of one or multiple RPCs"""
    client_done: bool
    rpcs: List[RPC]

    def __init__(self):
        self.client_done = False
        self.rpcs = []

    def __repr__(self):
        return textwrap.dedent(f"""
        Connection(
            {'''
            '''.join(repr(x) for x in self.rpcs)}
        )""").strip()


class Sessions:
    """
    A defaultdict-like session collection.
    """
    connections: MutableMapping[Hashable, Session]
    cookie_session: MutableMapping[Hashable, Session]

    def __init__(self):
        self.connections = {}
        self.cookie_sessions = {}

    def get(self, flow: http.HTTPFlow) -> Session:
        connection_id = (
            flow.client_conn.address[0],
            flow.server_conn.source_address[0],
            flow.client_conn.timestamp_start
        )
        if connection_id in self.connections:
            return self.connections[connection_id]

        cookies = dict(flow.request.cookies)
        cookies.update({k: v.value for k, v in flow.response.cookies.items()})
        session_id = (
            flow.client_conn.address[0],
            flow.server_conn.source_address[0],
            tuple(sorted(cookies.items()))
        )
        if cookies and session_id in self.cookie_sessions:
            return self.cookie_sessions[session_id]

        sess = Session()
        self.connections[connection_id] = sess
        if cookies:
            self.cookie_sessions[session_id] = sess
        return sess

    def all(self) -> List[Session]:
        # All entries in .cookie_sessions must also be in .connections, so this is enough.
        return list(self.connections.values())


class RPCSequencer:
    active_connections: Sessions
    flow_filter: flowfilter.TFilter

    def __init__(self, filt: str = ".*"):
        self.flow_filter = flowfilter.parse(filt)
        self.active_connections = Sessions()

    def request(self, flow: http.HTTPFlow):
        if not self.flow_filter(flow):
            return

        connection = self.active_connections.get(flow)

        if not connection.client_done:
            if flow.request.text:
                connection.rpcs.append(RPC(flow.request))
            else:
                connection.client_done = True
        else:
            connection.rpcs[-1].add_response(flow.request)

    def response(self, flow: http.HTTPFlow):
        if not self.flow_filter(flow):
            return

        connection = self.active_connections.get(flow)

        if not connection.client_done:
            connection.rpcs[-1].add_response(flow.response)
        else:
            if flow.response.text:
                try:
                    rpc = RPC(flow.response)
                except ValueError:
                    connection.client_done = False
                    raise
                else:
                    connection.rpcs.append(rpc)
            else:
                connection.client_done = False

    def done(self):
        print(self.active_connections.all())


def start():
    return RPCSequencer()
