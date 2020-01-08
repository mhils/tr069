"""
This script demonstrates how the client can send arbitrary RPCs.
"""
import tr069

# By default, our TR-069 client has no concept of state - it can
# send any RPC at any point in time. For example, we can send a
# GetRPCMethods command before sending the initial Inform as it
# would be required by the specification.
c = tr069.Client("https://acs.example.com/")
rpc_methods = c.get_rpc_methods()

# All transmitted RPCs are stored in client.messages:
assert c.messages == [rpc_methods]

# We can modify RPCs to e.g. form syntactically invalid requests.
# This:
c.request_download("3 Vendor Configuration File")
# is just syntactic sugar for the following:
xml = tr069.rpcs.make_request_download("3 Vendor Configuration File")
c.request(xml)
# The latter form provides full control over the bytes that will be sent.

# client.request accepts optional arguments that get passed to
# request's session.request(). This can be used to set headers and
# other options:
c.request(xml, headers={"Host": "example.org"})

# We can also replay a previous request *exactly* as-is.
# This is particularly useful to test if the server is invalidating
# digest authentication nonces.
c = tr069.Client("https://acs.example.com/", digest_auth=("user", "pass"))
resp = c.inform()
resp2 = c.replay(resp.request)
assert resp2.status_code != 200  # this must not work.

# Last, most server RPCs can be processed automatically using
# client.handle_server_rpcs().
# Unhandled RPCs raise a NotImplementedError:
c.done()  # signal the server that we are done sending RPCs.
try:
    c.handle_server_rpcs()
except NotImplementedError as e:
    print(e)
    print(c.messages[-1].text)  # print the full RPC contents
