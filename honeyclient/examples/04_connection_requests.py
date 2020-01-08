"""
The tr069 library contains a builtin Connection Request Server that can 
be used to observe connection requests by providers and react to them.
This script demonstrates its use.
"""
import time

import tr069

# The connection request server is a *minimal* HTTP server running
# in a background thread. It automatically accepts TCP connections
# on port 7547, replies with a predefined static response and prints
# a message to stdout indicating that a connection request has been
# handled.
serv = tr069.ConnectionRequestServer()

time.sleep(60)
# Running `curl localhost:7547` now produces the following output
# in the console:
#
#   === Connection request from 127.0.0.1 ===
#   GET / HTTP/1.1
#   Host: localhost:7547
#   User-Agent: curl/7.46.0
#   Accept: */*

# The connection request server's predefined response tries to bait
# the requesting entity into sending credentials using basic auth.
# The requesting entity should refuse this as this would allow
# a man-in-the-middle attacker to conduct replay attacks.

# It is also possible to wait for a connection request in the main
# thread:
s = tr069.ConnectionRequestServer()
sock, addr = s.queue.get()
print(f"Received connection request from {addr}!")
