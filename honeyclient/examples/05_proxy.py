"""
This script shows how proxy support can be enabled.
"""
import tr069

# Route all requests through a mitmproxy instance listening on
# port 8080. As certificates are verified by default, we need to
# pass the mitmproxy CA explicitly.
tr069.proxy.enable(
    "http://localhost:8080/",
    "~/.mitmproxy/mitmproxy-ca-cert.pem"
)

# Proxying can be disabled like so:
tr069.proxy.disable()
