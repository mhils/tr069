import mock
import pytest
import requests

from tr069 import Client


def test_init():
    c = Client("http://acs.example.com/", basic_auth=("foo", "bar"))
    assert c.requests_kwargs["auth"]
    c = Client("http://acs.example.com/", digest_auth=("foo", "bar"))
    assert c.requests_kwargs["auth"]
    c = Client("http://acs.example.com/", cert="certfile")
    assert c.requests_kwargs["cert"]
    with pytest.raises(ValueError):
        Client("http://acs.example.com/", basic_auth=("foo", "bar"), digest_auth=("foo", "bar"))


def test_basic(client: Client, capsys):
    assert repr(client) == "tr069.Client(http://acs.example.com/, 0 messages)"

    assert client.request("qux")
    assert client.messages
    assert not capsys.readouterr()[0]

    client.log = True
    assert client.request("qux")
    assert capsys.readouterr()[0]

    client.close()
    assert isinstance(client._session, requests.Session)


def test_rpcs(client: Client):
    assert client.get_rpc_methods()
    assert client.inform()
    assert client.request_download()
    assert client.set_parameter_values_response()
    assert client.get_parameter_values_response()
    assert client.set_parameter_attributes_response()
    assert client.get_parameter_names_response()
    assert client.done()


def test_handle_server_rpcs(client: Client):
    """Properly handle all known RPCs and terminate on 204"""
    get_parameter_names = mock.MagicMock()
    get_parameter_names.text = """
        <soapenv:Body>
            <cwmp:GetParameterNames>
                <ParameterPath>InternetGatewayDevice.</ParameterPath>
                <NextLevel>0</NextLevel>
            </cwmp:GetParameterNames>
        </soapenv:Body>
    """
    set_parameter_values = mock.MagicMock()
    set_parameter_values.text = """
        <soapenv:Body>
            <cwmp:SetParameterValues>
                <ParameterList soap:arrayType="cwmp:ParameterValueStruct[1]">
                    <ParameterValueStruct>
                        <Name>Foo</Name>
                        <Value>Bar</Value>
                    </ParameterValueStruct>
                </ParameterList>
            </cwmp:SetParameterValues>
        </soapenv:Body>
    """
    get_parameter_values = mock.MagicMock()
    get_parameter_values.text = """
        <soapenv:Body>
            <cwmp:GetParameterValues>
                <ParameterNames soap:arrayType="xsd:string[1]">
                    <string>Foo</string>
                </ParameterNames>
            </cwmp:GetParameterValues>
        </soapenv:Body>
    """
    set_parameter_attributes = mock.MagicMock()
    set_parameter_attributes.text = """
        <soapenv:Body>
        <cwmp:SetParameterAttributes>
          <ParameterList SOAP-ENC:arrayType="cwmp:SetParameterAttributesStruct[1]">
            <SetParameterAttributesStruct>
              <Name>InternetGatewayDevice.LANDevice.1.LANHostConfigManagement.DHCPServerEnable</Name>
              <NotificationChange>1</NotificationChange>
              <Notification>1</Notification>
              <AccessListChange>0</AccessListChange>
              <AccessList SOAP-ENC:arrayType="xsd:string[0]"></AccessList>
            </SetParameterAttributesStruct>
          </ParameterList>
        </cwmp:SetParameterAttributes>
        </soapenv:Body>
    """
    done = mock.MagicMock()
    done.status_code = 204
    client._session.post.side_effect = [
        get_parameter_names,
        set_parameter_values,
        get_parameter_values,
        set_parameter_attributes,
        done
    ]
    client.done()
    assert client.handle_server_rpcs() == 4
    assert client.device.params["Foo"].value == "Bar"


def test_handle_server_rpcs_unknown_rpc(client: Client):
    """Raise a NotImplementedError if we don't know the RPC"""
    unknown = mock.MagicMock()
    unknown.text = "<soap:Body><cwmp:Unknown />"
    client._session.post.side_effect = [
        unknown
    ]
    client.done()
    with pytest.raises(NotImplementedError):
        client.handle_server_rpcs()


def test_replay(client: Client):
    assert client.get_rpc_methods()
    assert client.replay()
    assert client.replay(client.messages[0])
