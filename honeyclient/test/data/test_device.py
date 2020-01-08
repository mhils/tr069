import os
import textwrap

import pytest

from tr069 import device

here = os.path.abspath(os.path.dirname(__file__))


def test_from_xml():
    with pytest.raises(Exception):
        device.from_xml("")
    d = device.from_xml("""
<DeviceId>
    <Manufacturer>AVM</Manufacturer>
    <OUI>00040E</OUI>
    <ProductClass>FRITZ!Box</ProductClass>
    <SerialNumber>001A4FFAFFFE</SerialNumber>
</DeviceId>
<ParameterValueStruct>
    <Name>InternetGatewayDevice.DeviceInfo.Manufacturer</Name>
    <Value xsi:type="xsd:string">AVM</Value>
</ParameterValueStruct>
""")
    assert d.manufacturer == "AVM"
    assert d.oui == "00040E"
    assert d.product_class == "FRITZ!Box"
    assert d.serial == "001A4FFAFFFE"
    assert d.params["InternetGatewayDevice.DeviceInfo.Manufacturer"].value == "AVM"


def test_device_to_xml():
    d = device.Device(
        "foo",
        "bar",
        "baz",
        "qux",
    )
    assert repr(d) == 'Device(foo baz, Serial: qux, 0 parameters)'
    assert d.to_xml() == textwrap.dedent('''
        <DeviceId>
            <Manufacturer>foo</Manufacturer>
            <OUI>bar</OUI>
            <ProductClass>baz</ProductClass>
            <SerialNumber>qux</SerialNumber>
        </DeviceId>
    ''').strip()


def test_capture():
    with open(os.path.join(here, "capture.txt"), "r") as f:
        xml = f.read()
    assert device.from_xml(xml)
