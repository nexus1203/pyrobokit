from pyrobokit.tcp_transport import TcpTransport
from pyrobokit.tcp_transport import API_PORT_OTHER
import time

ip_address = "192.168.11.191"
fork_control_req = 6040

transport = TcpTransport(ip_address, API_PORT_OTHER)
print(transport.connected)

data = {"height": 0.03}  #m
data = transport.send_n_receive(0, fork_control_req, data)
print("response:: ", data)
time.sleep(3)

data = {"height": 0.00}  #m
data = transport.send_n_receive(0, fork_control_req, data)
print("response:: ", data)
time.sleep(3)