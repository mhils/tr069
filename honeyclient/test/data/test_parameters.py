import textwrap

import pytest

from tr069 import parameters


class TestParameters:
    def test_get(self):
        p = parameters.Parameters(foo="bar")
        assert p["foo"].value == "bar"

    def test_set(self):
        p = parameters.Parameters()
        p["foo"] = "bar"
        assert p["foo"].value == "bar"
        p["baz"] = parameters.Parameter("baz", "qux")
        assert p["baz"].value == "qux"
        with pytest.raises(ValueError):
            p["qux"] = parameters.Parameter("other", "quux")
        with pytest.raises(TypeError):
            p["qux"] = 42

    def test_del(self):
        p = parameters.Parameters(foo="bar")
        del p["foo"]
        assert "foo" not in p

    def test_iter(self):
        p = parameters.Parameters(foo="bar")
        assert len(list(p)) == 1

    def test_len(self):
        p = parameters.Parameters(foo="bar")
        assert len(p) == 1

    def test_repr(self):
        p = parameters.Parameters(foo="bar", bar="boo")
        assert repr(p) == "Parameters(2 values)"

    def test_str(self):
        p = parameters.Parameters(foo="bar")
        assert str(p) == textwrap.dedent("""
        Parameters({
            "foo": "bar"
        })
        """).strip()

    def test_all(self):
        p = parameters.Parameters(**{
            "foo.foo": "bar",
            "foo.foobar": "baz",
            "bar": "bazoo",
        })
        assert len(p.all()) == 3
        assert len(p.all("foo.")) == 2
        assert len(p.all("foo.foo")) == 1


def test_from_xml():
    assert len(parameters.from_xml("")) == 0
    params = parameters.from_xml("""
    <ParameterValueStruct>
<Name>InternetGatewayDevice.ManagementServer.ConnectionRequestURL</Name>
<Value xsi:type="xsd:string">http://192.168.99.100:80/76bdab54</Value>
</ParameterValueStruct>
""")
    param = params["InternetGatewayDevice.ManagementServer.ConnectionRequestURL"]
    assert param.name == "InternetGatewayDevice.ManagementServer.ConnectionRequestURL"
    assert param.value == "http://192.168.99.100:80/76bdab54"
    assert param.type == "xsd:string"


class TestParameter:
    def test_to_xml(self):
        param = parameters.Parameter(
            "foo",
            "bar",
            "baz",
        )
        assert repr(param) == 'Parameter(foo: baz = "bar")'
        assert param.to_xml() == textwrap.dedent('''
        <ParameterValueStruct>
            <Name>foo</Name>
            <Value xsi:type="baz">bar</Value>
        </ParameterValueStruct>
        ''').strip()

    def test_to_info_xml(self):
        param = parameters.Parameter(
            "foo",
            "bar",
        )
        assert param.to_info_xml() == textwrap.dedent('''
        <ParameterInfoStruct>
            <Name>foo</Name>
            <Writable>1</Writable>
        </ParameterInfoStruct>
        ''').strip()
