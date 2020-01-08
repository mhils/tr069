TR069 Honeyclient API Reference
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TR-069 Client
-------------
.. py:currentmodule:: tr069

.. autoclass:: tr069.Client
	:no-members:

	.. automethod:: tr069.Client.request
	.. automethod:: tr069.Client.replay
	.. automethod:: tr069.Client.done
	.. automethod:: tr069.Client.handle_server_rpcs
	.. automethod:: tr069.Client.close

Remote Procedure Calls
**********************

For method signatures, see the RPC section below.

.. py:class:: Client

	.. automethod:: inform
	.. automethod:: get_rpc_methods
	.. automethod:: request_download
	.. automethod:: set_parameter_values_response
	.. automethod:: get_parameter_values_response
	.. automethod:: set_parameter_attributes_response
	.. automethod:: get_parameter_names_response

Connection Request Server
-------------------------

.. autoclass:: tr069.ConnectionRequestServer

Proxy Support
-------------

.. automodule:: tr069.proxy

Devices
-------

.. automodule:: tr069.data.device
	:no-members:

	.. autoclass:: tr069.data.device.Device

	.. automethod:: tr069.data.device.from_xml

	.. autodata:: tr069.data.device.AVM_FRITZ_BOX_7490
		:annotation:
	.. autodata:: tr069.data.device.FREECWMP
		:annotation:
	.. autodata:: tr069.data.device.DEFAULT
		:annotation:

Inform Events
-------------

.. automodule:: tr069.data.event
	:no-members:

	.. autoclass:: tr069.data.event.Event

	.. autodata:: tr069.data.event.Bootstrap
		:annotation:
	.. autodata:: tr069.data.event.Boot
		:annotation:
	.. autodata:: tr069.data.event.Periodic
		:annotation:
	.. autodata:: tr069.data.event.Scheduled
		:annotation:
	.. autodata:: tr069.data.event.ValueChange
		:annotation:
	.. autodata:: tr069.data.event.Kicked
		:annotation:
	.. autodata:: tr069.data.event.ConnectionRequest
		:annotation:
	.. autodata:: tr069.data.event.TransferComplete
		:annotation:
	.. autodata:: tr069.data.event.DiagnosticsComplete
		:annotation:
	.. autodata:: tr069.data.event.RequestDownload
		:annotation:
	.. autodata:: tr069.data.event.AutonomousTransferComplete
		:annotation:
	.. autodata:: tr069.data.event.DuStateChangeComplete
		:annotation:
	.. autodata:: tr069.data.event.AutonomousDuStateChangeComplete
		:annotation:
	.. autodata:: tr069.data.event.Wakeup
		:annotation:

Device Parameters
-----------------

.. automodule:: tr069.data.parameters

	.. automethod:: tr069.data.parameters.from_xml


Remote Procedure Calls
----------------------

.. automodule:: tr069.data.rpcs

requests.Response
----------------------

.. autoclass:: requests.models.Response
