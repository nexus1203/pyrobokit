from pyrobokit.tcp_transport import TcpTransport
from pyrobokit.tcp_transport import API_PORT_TASK
import time

ip_address = "192.168.11.191"
set_task_req = 3051

transport = TcpTransport(ip_address, API_PORT_TASK)
print(transport.connected)

#LM18->LM15
task_id = "LM15"
# go to LM15 with 0.3 m/s
now = 0.3
data = {"id": task_id, "max_speed": now}
data = transport.send_n_receive(0, set_task_req, data)
print("speed set:: ", data)
time.sleep(10)

task_id = "LM15"
# Stop after 6 secons
now = 0.0
data = {"id": task_id, "max_speed": now}
data = transport.send_n_receive(0, set_task_req, data)
print("speed set:: ", data)
time.sleep(5)

task_id = "LM18"
# come back to LM18
now = 0.3
data = {"id": task_id, "max_speed": now}
data = transport.send_n_receive(0, set_task_req, data)
print("speed set:: ", data)
# time.sleep(6)
