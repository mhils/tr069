from tr069.data import parameters
from tr069.data import rpcs


def test_parse_set_parameter_values():
    assert len(rpcs.parse_set_parameter_values("""
        <ParameterValueStruct>
            <Name>InternetGatewayDevice.ManagementServer.ConnectionRequestURL</Name>
            <Value xsi:type="xsd:string">http://192.168.99.100:80/76bdab54</Value>
        </ParameterValueStruct>
    """)) == 1


def test_make_set_parameter_values_response():
    assert rpcs.make_set_parameter_values_response(42)


def test_parse_get_parameter_values():
    assert rpcs.parse_get_parameter_values("""
        <cwmp:GetParameterValues>
            <ParameterNames soap:arrayType="xsd:string[1]">
                <string>foo</string>
            </ParameterNames>
        </cwmp:GetParameterValues>
    """) == ["foo"]


def test_make_get_parameter_values_response():
    assert rpcs.make_get_parameter_values_response([
        parameters.Parameter("foo", "bar")
    ])


def test_make_set_parameter_attributes_response():
    assert rpcs.make_set_parameter_attributes_response()


def test_parse_get_parameter_names():
    assert rpcs.parse_get_parameter_names("""
        <cwmp:GetParameterNames>
            <ParameterPath>InternetGatewayDevice.</ParameterPath>
            <NextLevel>0</NextLevel>
        </cwmp:GetParameterNames>
    """) == ("InternetGatewayDevice.", False)


def test_make_get_parameter_names_response():
    assert rpcs.make_get_parameter_names_response([
        parameters.Parameter("foo", "bar")
    ])
