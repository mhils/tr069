from typing import Collection, List, Tuple

from bs4 import BeautifulSoup

from .. import parameters
from .. import soap


def parse_set_parameter_values(xml: str) -> List[parameters.Parameter]:
    """
    Parse a SetParameterValues RPC

    Returns:
        List of parameters that should be updated.
    """
    return parameters.from_xml(xml).all()


def make_set_parameter_values_response(status: int = 0) -> str:
    """Create a SetParameterValuesResponse"""
    return soap.soapify(f"""
        <cwmp:SetParameterValuesResponse>
            <Status>{status}</Status>
        </cwmp:SetParameterValuesResponse>
    """)


def parse_get_parameter_values(xml: str) -> List[str]:
    """
    Parse a GetParameterValues RPC.

    Returns:
        List of requested parameters.
    """
    tree = BeautifulSoup(xml, "html.parser")
    params = tree.find("ParameterNames".lower()).find_all("string")
    return [x.get_text(strip=True) for x in params]


def make_get_parameter_values_response(params: Collection[parameters.Parameter] = ()) -> str:
    """Make a GetParameterValuesResponse"""
    return soap.soapify(f"""
        <cwmp:GetParameterValuesResponse>
            <ParameterList soap-enc:arrayType="cwmp:ParameterValueStruct[{len(params)}]">
                {"".join(parameter.to_xml() for parameter in params)}
            </ParameterList>
        </cwmp:GetParameterValuesResponse>
    """)


def make_set_parameter_attributes_response() -> str:
    """Make a SetParameterAttributesResponse"""
    return soap.soapify("<cwmp:SetParameterAttributesResponse />")


def parse_get_parameter_names(xml: str) -> Tuple[str, bool]:
    """
    Parse a GetParameterNames RPC.

    Returns:
        A (path, next_level) tuple.
    """
    tree = BeautifulSoup(xml, "html.parser")
    path = tree.find("ParameterPath".lower()).get_text(strip=True)
    next_level = {
        "true": True,
        "1": True,
        "false": False,
        "0": False
    }[tree.find("NextLevel".lower()).get_text(strip=True).lower()]
    return path, next_level


def make_get_parameter_names_response(params: Collection[parameters.Parameter] = ()) -> str:
    """Make a GetParameterNamesResponse"""
    return soap.soapify(f"""
        <cwmp:GetParameterNamesResponse>
            <ParameterList soap-enc:arrayType="cwmp:ParameterInfoStruct[{len(params)}]">
                {"".join(parameter.to_info_xml() for parameter in params)}
            </ParameterList>
        </cwmp:GetParameterNamesResponse>
    """)
