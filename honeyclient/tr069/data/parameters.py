import collections.abc
import textwrap
from typing import List, Union, Dict, Iterable

from bs4 import BeautifulSoup

REQUIRED_INFORM_PARAMETERS = [
    "InternetGatewayDevice.DeviceSummary",
    "InternetGatewayDevice.DeviceInfo.SpecVersion",
    "InternetGatewayDevice.DeviceInfo.HardwareVersion",
    "InternetGatewayDevice.DeviceInfo.SoftwareVersion",
    "InternetGatewayDevice.DeviceInfo.ProvisioningCode",
    "InternetGatewayDevice.ManagementServer.ConnectionRequestURL",
    "InternetGatewayDevice.ManagementServer.ParameterKey",
    "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1.ExternalIPAddress",
]


class Parameter:
    """
    A TR-069 ParameterValueStruct.
    Represents a parameter on the device as specified by the TR-069 data models.
    """
    name: str
    value: str
    type: str
    notification_level: int

    def __init__(
            self,
            name,
            value,
            type="xsd:string",
            notification_level: int = 0,
            writable: bool = True,
    ):
        self.name = name
        self.value = value
        self.type = type
        self.notification_level = notification_level
        self.writable = writable

    def __repr__(self):
        type = (": " + self.type).replace(": xsd:string", "")
        notify = f"{self.notification_level}, " if self.notification_level else ""
        return f'Parameter({notify}{self.name}{type} = "{self.value}")'

    def to_xml(self) -> str:
        return textwrap.dedent(f"""
            <ParameterValueStruct>
                <Name>{self.name}</Name>
                <Value xsi:type="{self.type}">{self.value}</Value>
            </ParameterValueStruct>
        """).strip()

    def to_info_xml(self) -> str:
        return textwrap.dedent(f"""
            <ParameterInfoStruct>
                <Name>{self.name}</Name>
                <Writable>{int(self.writable)}</Writable>
            </ParameterInfoStruct>
        """).strip()


class Parameters(collections.abc.MutableMapping):
    """
    A collection of TR-069 parameters representing a device.
    """
    _dict: Dict[str, Parameter]

    def __init__(self, params: Iterable[Parameter] = (), **kwargs: Dict[str, str]):
        self._dict = {}
        for param in params:
            self[param.name] = param
        self.update(**kwargs)

    def __getitem__(self, key: str) -> Parameter:
        return self._dict[key]

    def __setitem__(self, key: str, value: Union[str, Parameter]):
        if isinstance(value, str):
            self._dict[key] = Parameter(key, value)
        elif isinstance(value, Parameter):
            if key != value.name:
                raise ValueError(f"Key ({key}) does not match parameter name ({value.name})")
            self._dict[key] = value
        else:
            raise TypeError(f"Expected str or Parameter, but got {type(value)} instead.")

    def __delitem__(self, key: str):
        del self._dict[key]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return f"Parameters({len(self._dict)} values)"

    def __str__(self):
        return textwrap.dedent(
            f"""
            Parameters({{
                {''',
                '''.join(f'"{p.name}": "{p.value}"' for p in self._dict.values())}
            }})"""
        ).strip()

    def all(self, key: str = "", min_notification_level: int = 0) -> List[Parameter]:
        """
        Returns:
            A list containing...
             - all parameter starting with the common prefix key, if key is empty or ends with a dot.
             - the requested parameter key.
        """
        if key == "" or key.endswith("."):
            matches = lambda param: param.startswith(key)
        else:
            matches = lambda param: param == key
        return [
            param
            for param in self._dict.values()
            if matches(param.name) and param.notification_level >= min_notification_level
        ]


def from_xml(xml: str) -> Parameters:
    """
    Construct a parameters object from XML that contains a ParameterValueStruct, 
    e.g., an Inform RPC.
    """
    tree = BeautifulSoup(xml, "html.parser")
    nodes = tree.find_all("ParameterValueStruct".lower())
    return Parameters(
        Parameter(
            node.find("name").get_text(strip=True),
            node.find("value").get_text(strip=True),
            node.find("value").get("xsi:type") or "xsd:string"
        )
            for node in nodes
    )
