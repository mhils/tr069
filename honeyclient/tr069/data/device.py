import textwrap
from typing import Optional

from bs4 import BeautifulSoup

from . import parameters


class Device:
    """
    A TR-069 Device.
    """
    manufacturer: str
    oui: str
    product_class: str
    serial: str
    params: parameters.Parameters

    def __init__(
            self,
            manufacturer,
            oui,
            product_class,
            serial,
            params: Optional[parameters.Parameters] = None
    ):
        self.manufacturer = manufacturer
        self.oui = oui
        self.product_class = product_class
        self.serial = serial
        if params is None:
            params = parameters.Parameters()
        self.params = params

        # better sphinx doc
        self.__doc__ = repr(self)

    def __repr__(self):
        return (
            f"Device({self.manufacturer} {self.product_class}, "
            f"Serial: {self.serial}, "
            f"{len(self.params)} parameters)"
        )

    def to_xml(self) -> str:
        return textwrap.dedent(f"""
            <DeviceId>
                <Manufacturer>{self.manufacturer}</Manufacturer>
                <OUI>{self.oui}</OUI>
                <ProductClass>{self.product_class}</ProductClass>
                <SerialNumber>{self.serial}</SerialNumber>
            </DeviceId>
        """).strip()


def from_xml(xml: str) -> Device:
    """Construct a device from an Inform XML."""
    tree = BeautifulSoup(xml, "html.parser")
    device = tree.find("DeviceId".lower())
    m, o, p, s = [
        device.find(x.lower()).get_text(strip=True)
        for x in ["Manufacturer", "OUI", "ProductClass", "SerialNumber"]
    ]
    params = parameters.from_xml(xml)
    return Device(
        m, o, p, s, params
    )


# Taken from https://www.redteam-pentesting.de/en/advisories/rt-sa-2015-005/-o2-telefonica-germany-acs-discloses-voip-sip-credentials
AVM_FRITZ_BOX_7490 = from_xml("""
    <cwmp:Inform>
    <DeviceId>
        <Manufacturer>AVM</Manufacturer>
        <OUI>00040E</OUI>
        <ProductClass>FRITZ!Box</ProductClass>
        <SerialNumber>0896D776FAA2</SerialNumber>
    </DeviceId>
    <Event soap-enc:arrayType="cwmp:EventStruct[3]">
        <EventStruct>
            <EventCode>4 VALUE CHANGE</EventCode>
            <CommandKey></CommandKey></EventStruct>
        <EventStruct>
            <EventCode>1 BOOT</EventCode>
            <CommandKey></CommandKey></EventStruct>
        <EventStruct>
            <EventCode>0 BOOTSTRAP</EventCode>
            <CommandKey></CommandKey></EventStruct>
    </Event>
    <MaxEnvelopes>1</MaxEnvelopes>
    <CurrentTime>2017-02-01T22:57:23+01:00</CurrentTime>
    <RetryCount>0</RetryCount>
    <ParameterList soap-enc:arrayType="cwmp:ParameterValueStruct[8]">
        <ParameterValueStruct>
            <Name>InternetGatewayDevice.DeviceSummary</Name>
            <Value xsi:type="xsd:string">InternetGatewayDevice:1.4[](Baseline:2, EthernetLAN:1, ADSLWAN:1, ADSL2WAN:1, Time:2, IPPing:1, WiFiLAN:2, DeviceAssociation:1), VoiceService:1.0[2](SIPEndpoint:1, Endpoint:1, TAEndpoint:1), StorageService:1.0[1](Baseline:1, FTPServer:1, NetServer:1, HTTPServer:1, UserAccess:1, VolumeConfig:1)</Value>
        </ParameterValueStruct>
        <ParameterValueStruct>
            <Name>InternetGatewayDevice.DeviceInfo.HardwareVersion</Name>
            <Value xsi:type="xsd:string">FRITZ!Box 7490</Value>
        </ParameterValueStruct>
        <ParameterValueStruct>
            <Name>InternetGatewayDevice.DeviceInfo.SoftwareVersion</Name>
            <Value xsi:type="xsd:string">113.06.20</Value>
        </ParameterValueStruct>
        <ParameterValueStruct>
            <Name>InternetGatewayDevice.DeviceInfo.SpecVersion</Name>
            <Value xsi:type="xsd:string">1.0</Value>
        </ParameterValueStruct>
        <ParameterValueStruct>
            <Name>InternetGatewayDevice.DeviceInfo.ModelName</Name>
            <Value xsi:type="xsd:string">Router Fritz!Box 7490</Value>
        </ParameterValueStruct>
        <ParameterValueStruct>
            <Name>InternetGatewayDevice.DeviceInfo.Manufacturer</Name>
            <Value xsi:type="xsd:string">AVM</Value>
        </ParameterValueStruct>
        <ParameterValueStruct>
            <Name>InternetGatewayDevice.DeviceInfo.ManufacturerOUI</Name>
            <Value xsi:type="xsd:string">00040E</Value>
        </ParameterValueStruct>
        <ParameterValueStruct>
            <Name>InternetGatewayDevice.DeviceInfo.ProvisioningCode</Name>
            <Value xsi:type="xsd:string">000.000.000.000</Value></ParameterValueStruct>
        </ParameterValueStruct>
        <ParameterValueStruct>
            <Name>InternetGatewayDevice.ManagementServer.ParameterKey</Name>
            <Value xsi:type="xsd:string">null</Value>
        </ParameterValueStruct>
        <ParameterValueStruct>
            <Name>InternetGatewayDevice.ManagementServer.ConnectionRequestURL</Name>
            <Value xsi:type="xsd:string"></Value>
        </ParameterValueStruct>
        <ParameterValueStruct>
            <Name>InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1.ExternalIPAddress</Name>
            <Value xsi:type="xsd:string"></Value>
        </ParameterValueStruct>
    </ParameterList>
    </cwmp:Inform>
""")

# OpenWRT with freecwmp (default configuration)
FREECWMP = from_xml("""
<cwmp:Inform><DeviceId><Manufacturer>freecwmp</Manufacturer><OUI>FFFFFF</OUI><ProductClass>freecwmp</ProductClass><SerialNumber>FFFFFF123456</SerialNumber></DeviceId><Event
soap_enc:arrayType="cwmp:EventStruct[2]"><EventStruct><EventCode>0 BOOTSTRAP</EventCode><CommandKey /></EventStruct><EventStruct><EventCode>1 BOOT</EventCode><CommandKey /></EventStruct></Event><MaxEnvelopes>1</MaxEnvelopes><CurrentTime>2017-01-09T17:40:23+0000</CurrentTime><RetryCount>1</RetryCount><ParameterList
soap_enc:arrayType="cwmp:ParameterValueStruct[11]"><ParameterValueStruct><Name>InternetGatewayDevice.DeviceInfo.SpecVersion</Name>
<Value xsi:type="xsd:string">1.0</Value></ParameterValueStruct><ParameterValueStruct><Name>InternetGatewayDevice.DeviceInfo.Manufacturer</Name>
<Value xsi:type="xsd:string">freecwmp</Value></ParameterValueStruct><ParameterValueStruct><Name>InternetGatewayDevice.DeviceInfo.ManufacturerOUI</Name>
<Value xsi:type="xsd:string">FFFFFF</Value></ParameterValueStruct><ParameterValueStruct><Name>InternetGatewayDevice.DeviceInfo.ProductClass</Name>
<Value xsi:type="xsd:string">freecwmp</Value></ParameterValueStruct><ParameterValueStruct><Name>InternetGatewayDevice.DeviceInfo.SerialNumber</Name>
<Value xsi:type="xsd:string">FFFFFF123456</Value></ParameterValueStruct><ParameterValueStruct><Name>InternetGatewayDevice.DeviceInfo.HardwareVersion</Name>
<Value xsi:type="xsd:string">example_hw_version</Value></ParameterValueStruct><ParameterValueStruct><Name>InternetGatewayDevice.DeviceInfo.SoftwareVersion</Name>
<Value xsi:type="xsd:string">example_sw_version</Value></ParameterValueStruct><ParameterValueStruct><Name>InternetGatewayDevice.DeviceInfo.ProvisioningCode</Name>
<Value xsi:type="xsd:string" /></ParameterValueStruct><ParameterValueStruct><Name>InternetGatewayDevice.ManagementServer.ParameterKey</Name>
<Value xsi:type="xsd:string" /></ParameterValueStruct><ParameterValueStruct><Name>InternetGatewayDevice.ManagementServer.ConnectionRequestURL</Name>
<Value xsi:type="xsd:string" /></ParameterValueStruct><ParameterValueStruct><Name>InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1.ExternalIPAddress</Name>
<Value xsi:type="xsd:string" /></ParameterValueStruct></ParameterList></cwmp:Inform>
""")

DEFAULT = AVM_FRITZ_BOX_7490
