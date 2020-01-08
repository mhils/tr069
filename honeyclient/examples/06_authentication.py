"""
This script demonstrates how different authentication options 
can be used.
"""
import tr069

url = "https://acs.example.com/"

# Basic and digest authentication can be enabled like this:
c_basic = tr069.Client(url, basic_auth=("user", "pass"))
c_digest = tr069.Client(url, digest_auth=("user", "pass"))

# TLS client certificates can be used as well, either as a single
# file (containing both private key and certificate) or as a
# (cert, key) tuple of file paths:
c_client_cert = tr069.Client(url, cert=("client.crt", "client.key"))

# Configuration servers also often use the device serial number for
# authentication. It can be changed like so:
c_basic.device.serial = "FFFFFF123456"
