from pyrobokit.agv_api import status
from time import sleep

ip = "192.168.0.10"

status_api = status.StatusAPI(ip=ip)

# qquery the navigation status

nav_status = Status.StatusNavigation()
success = status_api.get_status(nav_status)
print(nav_status.task_status)
print(nav_status.finished_path)

pose = status.StatusPose()
success = status_api.get_status(pose)
print(pose.x, pse.y, pose.angle, pose.confidence)
print(pose.current_station, pose.last_station)

