from pyrobokit.tcp_transport import TcpTransport
from pyrobokit.tcp_transport import API_PORT_TASK
import time

ip_address = "192.168.11.191"
set_task_req = 3051

transport = TcpTransport(ip_address, API_PORT_TASK)
print(transport.connected)

task_id = "AP14"

time.sleep(0.25)

# continue to decrease velocity
now = 0.3
for i in range(2):

    data = {"id": task_id, "max_speed": round(now / (i + 1), 3)}
    data = transport.send_n_receive(0, set_task_req, data)
    print("speed set:: ", data)
    time.sleep(6)
