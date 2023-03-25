from seer_robokit.agv_api import Notification
from time import sleep
from time import perf_counter as pf

ip = "192.168.11.191"
notify = Notification(ip)

notify.configure_monitoring(interval=500)

for i in range(1000):
    start = pf()
    data = notify.receive()
    print(f"interval:: {pf()-start}")
    print(data)