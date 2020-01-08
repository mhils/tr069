from mitmproxy.http import HTTPResponse
from tr069monitor import retain_reconfiguration


def test_set_parameter():
    resp = HTTPResponse.make(
        content="""
       <Name>Foo</Name>
       <Value>Bar</Value>
        """.strip()
    )
    retain_reconfiguration.set_parameter(
        resp,
        "foo",
        "baz"
    ) == """
       <Name>Foo</Name>
       <Value>baz</Value>
        """.strip()


def test_set_parameter_malformed():
    # I know this looks contrived, but this is an actual example we've seen in practice.
    resp = HTTPResponse.make(
        content="""
        <ParameterValueStruct>
           <Name>InternetGatewayDevice.ManagementServer.ConnectionRequestURL</Name>

           <Value xsi:type="xsd:string">http://194.175.125.104:8089/4b123c06</ Value="Value">
        </ParameterValueStruct>
        """.strip()
    )
    retain_reconfiguration.set_parameter(
        resp,
        "InternetGatewayDevice.ManagementServer.ConnectionRequestURL",
        "foo"
    ) == """
        <ParameterValueStruct>
           <Name>InternetGatewayDevice.ManagementServer.ConnectionRequestURL</Name>

           <Value xsi:type="xsd:string">foo</ Value="Value">
        </ParameterValueStruct>
        """.strip()
