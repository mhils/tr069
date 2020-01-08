"""
This script showcases how devices and device parameters are handled.
"""
import tr069

# By default, our TR-069 client emulates an AVM Fritz!Box 7490
# router. We can pass another device when constructing the client:
c = tr069.Client(
    "https://acs.example.com/",
    device=tr069.device.FREECWMP
)
# If we now call c.inform(), the client will identify itself as a
# freecwmp client in the Inform RPC.

# The device data structure stores information about the device
# itself as well as its parameters:
print(c.device)
print(c.device.params)

# We can directly modify device attributes:
c.device.params["InternetGatewayDevice.DeviceInfo.ProvisioningCode"] = "1234"

# Devices can be constructed manually with tr069.device.Device().
# More comfortably, we can also create a device from intercepted traffic:
with open("test/data/capture.txt") as f:
    xml = f.read()  # contains an intercepted Inform RPC

device = tr069.device.from_xml(xml)
print(device)
