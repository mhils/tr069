import io
from typing import Mapping, Any, Callable

import requests

from mitmproxy import http
from mitmproxy.io import FlowWriter
import anonymize


class FlowLogger:
    endpoint: str
    request_kwargs = Mapping[str, Any]
    flow_preprocessor: Callable[[http.HTTPFlow], http.HTTPFlow]

    def __init__(self, endpoint, flow_preprocessor=lambda x: x, request_kwargs=None):
        if request_kwargs is None:
            request_kwargs = {}
        self.endpoint = endpoint
        self.flow_preprocessor = flow_preprocessor
        self.request_kwargs = request_kwargs
        self.session = requests.Session()

    def response(self, flow):
        flow = self.flow_preprocessor(flow)
        f = io.BytesIO()
        fw = FlowWriter(f)
        fw.add(flow)
        serialized = f.getvalue()
        self.session.post(
            self.endpoint,
            data=serialized,
            **self.request_kwargs
        )
        print(".", end="", flush=True)

    error = response


def start():
    def redact_flow(flow: http.HTTPFlow):
        flow = flow.copy()
        anonymize.redact(flow.request)
        if flow.response:
            anonymize.redact(flow.response)
        return flow

    return FlowLogger("https://collector/", redact_flow)
