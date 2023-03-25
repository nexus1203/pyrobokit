# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║ File:           push_notification.py                     ║
║ Author:         Kumar                                    ║
║ Created:        2023-03-23                               ║
║ Last Modified:  2023-03-23                               ║
║ Description:                                             ║  
╚══════════════════════════════════════════════════════════╝
"""

from ..tcp_transport import TcpTransport
from ..tcp_transport import API_PUSH_PORT
from threading import Thread


class Notification:

    def __init__(self, ip, port=API_PUSH_PORT):
        self.ip = ip
        self.port = port
        self.transport = TcpTransport(ip, port)
        self.transport.connect()

    def send(self, msg):
        """_summary_

        Args:
            msg (_type_): message should contain a json object or dictionary
            
            of objects that has to bbe added to the monitoring list
        """
        self.transport.send(msg)

    def configure_monitoring(self,
                             interval=1000,
                             parameters=["x", "y", "w"],
                             defaults=True):
        """
        Args:
            interval (int): interval in milliseconds
            parameters (list): list of parameters to be monitored
            defaults (bool): if True, the default parameters will be added to the list
        """
        if defaults:
            parameters = [
                "x", "y", "angle", "confidence", "vx", "vy", "w",
                "current_station", "is_stop", "fork", "target_point",
                "target_label", "target_id", "target_dist", "task_staus",
                "running_status", "task_type", "emergency", "charging",
                "battery_level", "map", "battery_temp", "voltage", "current"
            ]

        msg = {"interval": interval, "included_fields": parameters}
        self.transport.send_command(1, 9300, msg)
        data = self.transport.listen()
        print(data)

    def receive(self):
        return self.transport.listen()

    def close(self):
        self.transport.close()


if __name__ == "__main__":
    notification = Notification("127.0.0.1")
    notification.configure_monitoring()
    while True:
        data = notification.receive()
        print(data)