import textwrap
from typing import List

from bs4 import BeautifulSoup


class Event:
    """
    A TR-069 EventStruct.
    Represents an event that caused a TR-069 connection.
    """
    code: str
    command_key: str

    def __init__(self, code, command_key=""):
        self.code = code
        self.command_key = command_key

        # Better sphinx doc
        self.__doc__ = repr(self)

    def __repr__(self):
        return f"Event({self.code})"

    def to_xml(self) -> str:
        return textwrap.dedent(f"""
            <EventStruct>
                <EventCode>{self.code}</EventCode>
                <CommandKey>{self.command_key}</CommandKey>
            </EventStruct>
        """).strip()


def from_xml(xml: str) -> List[Event]:
    tree = BeautifulSoup(xml, "html.parser")
    nodes = tree.find_all("EventStruct".lower())
    return [
        Event(
            node.find("eventcode").get_text(strip=True),
            node.find("commandkey").get_text(strip=True),
        )
        for node in nodes
    ]


Bootstrap = Event("0 BOOTSTRAP")
Boot = Event("1 Boot")
Periodic = Event("2 PERIODIC")
Scheduled = Event("3 SCHEDULED")
ValueChange = Event("4 VALUE CHANGE")
Kicked = Event("5 KICKED")
ConnectionRequest = Event("6 CONNECTION REQUEST")
TransferComplete = Event("7 TRANSFER COMPLETE")
DiagnosticsComplete = Event("8 DIAGNOSTICS COMPLETE")
RequestDownload = Event("9 REQUEST DOWNLOAD")
AutonomousTransferComplete = Event("10 AUTONOMOUS TRANSFER COMPLETE")
DuStateChangeComplete = Event("11 DU STATE CHANGE COMPLETE")
AutonomousDuStateChangeComplete = Event("12 AUTONOMOUS DU STATE CHANGE COMPLETE")
Wakeup = Event("13 WAKEUP")
