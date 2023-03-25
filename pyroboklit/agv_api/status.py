# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║ File:           status.py                                ║
║ Author:         Nexus1203                                ║
║ Created:        2023-03-23                               ║
║ Last Modified:  2023-03-23                               ║
║ Description:    Status port features of robotkit api     ║  
╚══════════════════════════════════════════════════════════╝
"""

from ..tcp_transport import TcpTransport
from ..tcp_transport import API_PORT_STATE
import time


class Battery:

    def __init__(self, ):
        self.requestId = 0
        self.messageType = 1007  # battery status query
        self.msg = {}

        self.live = False

        self.level = 0
        self.temp = 0
        self.charging = False
        self.voltage = 0
        self.current = 0
        self.power = 0  # voltage * current
        self.max_charge_voltage = 0
        self.max_charge_current = 0
        self.manual_charge = False
        self.auto_charge = False
        self.battery_cycle = 0
        self.api_timestamp = 0
        self.err_msg = ""
        self.ret_code = 0
        self.json_data = {}

    def get_status(self, transport):
        self.live = False
        # self.msg = {"simple": "no"}  # get all battery status
        # send command and receive data
        data = transport.send_n_receive(self.requestId, self.messageType,
                                        self.msg)
        # parse data
        self.json_data = data
        if data["ret_code"] == 0:
            self.level = data["battery_level"]
            self.api_timestamp = data["create_on"]
            self.temp = data["battery_temp"]
            self.voltage = data["voltage"]
            self.current = data["current"]
            self.max_charge_voltage = data["max_charge_voltage"]
            self.max_charge_current = data["max_charge_current"]
            self.manual_charge = data["manual_charge"]
            self.auto_charge = data["auto_charge"]
            self.battery_cycle = data["battery_cycle"]
            self.power = self.voltage * self.current
            self.live = True
        else:
            self.err_msg = data["err_msg"]


class AGV_Pose:

    def __init__(self, ):
        self.requestId = 0
        self.messageType = 1004  # robot position query
        self.msg = {}  # empty message

        # AGV position attributes
        self.live = False
        self.x = 0
        self.y = 0
        self.angle = 0
        self.confidence = 0
        self.current_station = ""
        self.last_station = ""
        self.api_timestamp = ""
        self.json_data = {}

    def get_status(self, transport):

        self.live = False
        # send command and receive data
        data = transport.send_n_receive(self.requestId, self.messageType,
                                        self.msg)
        # parse data
        self.json_data = data
        if data["ret_code"] == 0:
            self.x = data["x"]
            self.y = data["y"]
            self.angle = data["angle"]
            self.confidence = data["confidence"]
            self.current_station = data["current_station"]
            self.last_station = data["last_station"]
            self.api_timestamp = data["create_on"]
            self.live = True
        else:
            self.err_msg = data["err_msg"]


class AGV_Speed:

    def __init__(self) -> None:
        self.requestId = 0
        self.messageType = 1005  # robot speed query
        self.msg = {}  # empty message

        # AGV speed attributes
        self.live = False
        self.vx = 0
        self.vy = 0
        self.w = 0
        self.steer = 0
        self.spin = 0
        self.r_vx = 0
        self.r_vy = 0
        self.r_w = 0
        self.r_steer = 0
        self.r_spin = 0
        self.steer_angle = 0
        self.is_stop = False

    def get_status(self, transport):
        self.live = False
        # send command and receive data
        data = transport.send_n_receive(self.requestId, self.messageType,
                                        self.msg)
        # parse data
        self.json_data = data
        if data["ret_code"] == 0:
            self.vx = data["vx"]
            self.vy = data["vy"]
            self.w = data["w"]
            self.steer = data["steer"]
            self.spin = data["spin"]
            self.r_vx = data["r_vx"]
            self.r_vy = data["r_vy"]
            self.r_w = data["r_w"]
            self.r_steer = data["r_steer"]
            self.r_spin = data["r_spin"]
            self.steer_angle = data["steer_angles"]
            self.is_stop = data["is_stop"]
            self.live = True
        else:
            self.err_msg = data["err_msg"]


class Forklift:

    def __init__(self) -> None:
        self.requestId = 0
        self.messageType = 1028  # forklift status query
        self.msg = {}  # empty message

        # forklift status attributes
        self.live = False
        self.fork_height = 0
        self.fork_height_in_place = False
        self.fork_auto_flag = False
        self.forward_val = 0
        self.forward_in_place = False
        self.fork_pressure_actual = 0
        self.json_data = {}

    def get_status(self, transport):
        self.live = False
        # send command and receive data
        transport.send_command(self.requestId, self.messageType, self.msg)
        data = transport.listen()
        # parse data
        self.json_data = data
        if data["ret_code"] == 0:
            self.fork_height = data["fork_height"]
            self.fork_height_in_place = data["fork_height_in_place"]
            self.fork_auto_flag = data["fork_auto_flag"]
            self.forward_val = data["forward_val"]
            self.forward_in_place = data["forward_in_place"]
            self.fork_pressure_actual = data["fork_pressure_actual"]
            self.live = True
        else:
            self.err_msg = data["err_msg"]


class Status:

    def __init__(self, ip, port=API_PORT_STATE) -> None:
        """_summary_

        Args:
            ip (_type_): AGV ip address
            port (_type_, optional): _description_. Defaults to API_PORT_STATE.
        """
        self.ip = ip
        self.port = port
        self.transport = TcpTransport(ip, port)
        self.battery = Battery()
        self.pose = AGV_Pose()
        self.speed = AGV_Speed()
        self.forklift = Forklift()

        self.connected = self.transport.connected

    def get_status(self):
        self.get_battery()
        # time.sleep(0.1)
        self.get_pose()
        # time.sleep(0.1)
        self.get_speed()
        # time.sleep(0.1)
        self.get_forklift()
        # time.sleep(0.1)

    def get_pose(self):
        self.pose.get_status(self.transport)

    def get_battery(self):
        self.battery.get_status(self.transport)

    def get_speed(self):
        self.speed.get_status(self.transport)

    def get_forklift(self):
        self.forklift.get_status(self.transport)
