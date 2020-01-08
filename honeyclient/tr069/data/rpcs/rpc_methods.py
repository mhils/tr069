from .. import soap


def make_get_rpc_methods() -> str:
    """Create a GetRPCMethods RPC"""
    return soap.soapify("<cwmp:GetRPCMethods />")
