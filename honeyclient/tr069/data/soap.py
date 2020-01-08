import re
import textwrap
from typing import Optional

CWMP_VERSION = "cwmp-1-0"
HEADER = '<cwmp:ID soap:mustUnderstand="1">1</cwmp:ID>'


def soapify(xml: str) -> str:
    """
    Wrap CWMP RPC in SOAP.
    """
    return textwrap.dedent(f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                       xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                       xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cwmp="urn:dslforum-org:{CWMP_VERSION}">
            <soap:Header>
                {HEADER}
            </soap:Header>
            <soap:Body>
                {xml}
            </soap:Body>
        </soap:Envelope>
    """).strip()


def extract_rpc_name(xml: str) -> Optional[str]:
    message_type = re.search(r"<[-\w]+:Body>\s*<(.+?)[ /]*>", xml, re.IGNORECASE)
    if message_type:
        return message_type.group(1)
    return None


cwmp_id_rex = re.compile(r"(<cwmp:ID[^>]*>)(.*?)(?=</cwmp:ID>)", re.IGNORECASE)


def get_cwmp_id(xml: str) -> Optional[str]:
    """Get a cwmp:ID from the provided xml"""
    cwmp_id = re.search(cwmp_id_rex, xml)
    if cwmp_id:
        return cwmp_id.group(2)
    return None


def set_cwmp_id(xml: str, cwmp_id: str) -> str:
    """Replace the cwmp:ID in xml with the provided one"""
    return re.sub(cwmp_id_rex, r"\g<1>" + cwmp_id, xml)


def fix_cwmp_id(xml: str, from_xml: str) -> str:
    """Replace the cwmp:ID in xml with the cwmp:ID in from_xml"""
    cwmp_id = get_cwmp_id(from_xml)
    if cwmp_id:
        return set_cwmp_id(xml, cwmp_id)
    return xml
