import datetime
import warnings
from typing import Optional, Collection

from .. import device
from .. import event as mevents
from .. import parameters
from .. import soap


def make_inform(
        *,
        device: device.Device,
        events: Collection[mevents.Event] = (
                mevents.ValueChange, mevents.Boot, mevents.Bootstrap
        ),
        params: Optional[Collection[parameters.Parameter]] = None,
        time: Optional[datetime.datetime] = None,
        retry_count: int = 0
) -> str:
    """Create a Inform RPC"""
    if time is None:
        time = datetime.datetime.now()
    if params is None:
        params = []
        for x in parameters.REQUIRED_INFORM_PARAMETERS:
            if x in device.params:
                params.append(device.params[x])
            else:
                warnings.warn(f"Missing required inform parameter: {x}")

    return soap.soapify(f"""
        <cwmp:Inform>
            {device.to_xml()}
            <Event soap-enc:arrayType="cwmp:EventStruct[{len(events)}]">
                {"".join(event.to_xml() for event in events)}
            </Event>
            <MaxEnvelopes>1</MaxEnvelopes>
            <CurrentTime>{time.isoformat()}</CurrentTime>
            <RetryCount>{retry_count}</RetryCount>
            <ParameterList soap-enc:arrayType="cwmp:ParameterValueStruct[{len(params)}]">
                {"".join(param.to_xml() for param in params)}
            </ParameterList>
        </cwmp:Inform>
    """)
