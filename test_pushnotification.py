from pyrobokit.agv_api import push_notification
from time import sleep
from time import perf_counter as pf

ip = "192.168.0.10"
notify = push_notification.Notification(ip)

notify.configure_monitoring(interval=1000) # keep it above 500 ms for stable response

for i in range(1000):
    start = pf()
    data = notify.receive()
    print(f"interval:: {pf()-start}")
    print(data)
    sleep(1)
