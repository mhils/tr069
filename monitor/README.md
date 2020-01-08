# TR-069 Monitor

The TR-069 monitor consists of the following scripts:

 - **`anonymize.py`**: A mitmproxy addon to redact sensitive information in TR-069 flows or reduce them entirely to their RPC name.
 - **`log_flows.py`**: A mitmproxy addon that sends all recorded flows to a central collector.
 - **`collector.py`**: A simple collector to receive and store TR-069 traffic from sensors.
 - **`retain_reconfiguration.py`**: A mitmproxy addon that dynamically rewrites TR-069 parameters between client and configuration server so that reconfigurations are retained.
 - **`sequence_rpcs.py`**: A TR-069 command sequencer that transforms a loose collection of HTTP flows into TR-069 (command, response) RPC tuples.

See `../docker-testenv` for usage examples.