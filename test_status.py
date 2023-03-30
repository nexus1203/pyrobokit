from pyrobokit.agv_api import Status
from time import sleep

ip = "192.168.11.191"

status = Status(ip=ip)

for i in range(1):
    # status.get_battery()
    # print(status.battery.json_data)
    # sleep(0.2)
    # status.get_pose()
    # print(status.pose.json_data)
    # sleep(0.2)
    # status.get_speed()
    # print(status.speed.json_data)
    # sleep(0.2)
    status.get_forklift()
    print(status.forklift.json_data)
    # sleep(0.2)
