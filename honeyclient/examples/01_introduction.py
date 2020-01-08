"""
This script provides an high-level overview
of the lifecycle of a TR-069 session.
"""
import tr069

# Create a TR-069 client with default device settings.
c = tr069.Client(
    "https://acs.example.com/",
    basic_auth=("user", "pass"),
    log=True  # print all messages to stdout
)

# Establish a connection with the ACS and send an initial Inform RPC
inform_response = c.inform()

# Inquire which RPC methods are supported by the ACS.
rpc_methods = c.get_rpc_methods()

# All RPCs return requests.Response objects.
print(rpc_methods.text)

# We need to indicate that we are done sending RPCs
# before the ACS starts sending commands.
c.done()

# Last, automatically handle all RPCs sent by the server.
command_count = c.handle_server_rpcs()
