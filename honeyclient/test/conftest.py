import mock
import pytest
import requests

import tr069


@pytest.fixture
def client():
    c = tr069.Client(
        "http://acs.example.com/",
        log=False
    )
    c._session = mock.MagicMock()
    c._session.post.return_value.text = "response"
    return c


@pytest.fixture()
def response():
    resp = requests.Response()
    resp.request = requests.Request(
        method="POST",
        url="http://acs.example.com/",
        headers={"foo": "bar"},
        data="qux"
    ).prepare()
    resp.status_code = 200
    resp.reason = "OK"
    resp.headers.update(bar="baz")
    resp._content = b"quux"
    return resp
