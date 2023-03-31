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
from .utils import check_success, to_json
import time


class StatusBattery:

    def __init__(self, ):
        """
        Battery status class
        """
        # API request data
        self.requestId = 0
        self.messageType = 1007  # battery status query
        self.msg = {}

        # battery status
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

        self.err_msg = ""
        self.success = False
        self.create_on = ""

        self.json_data = {}

    def _get_status(self, transport):
        # self.msg = {"simple": "no"}  # get all battery status
        # send command and receive data
        data = transport.send_n_receive(self.requestId, self.messageType,
                                        self.msg)
        # parse data
        self.json_data = data
        self.success = check_success(data)

        if self.success:
            self.level = data["battery_level"]
            self.temp = data["battery_temp"]
            self.voltage = data["voltage"]
            self.current = data["current"]
            self.max_charge_voltage = data["max_charge_voltage"]
            self.max_charge_current = data["max_charge_current"]
            self.manual_charge = data["manual_charge"]
            self.auto_charge = data["auto_charge"]
            self.battery_cycle = data["battery_cycle"]
            self.power = self.voltage * self.current
            self.create_on = data["create_on"]
        else:
            self.create_on = data["create_on"]
            self.err_msg = data["err_msg"]
        return self.success


class StatusPose:

    def __init__(self, ):
        # API request data
        self.requestId = 0
        self.messageType = 1004  # robot position query
        self.msg = {}  # empty message

        # AGV position attributes
        self.x = 0
        self.y = 0
        self.angle = 0
        self.confidence = 0
        self.current_station = ""
        self.last_station = ""

        self.success = False
        self.err_msg = 0
        self.create_on = ""

        self.json_data = {}

    def _get_status(self, transport):

        # send command and receive data
        data = transport.send_n_receive(self.requestId, self.messageType,
                                        self.msg)
        # parse data
        self.json_data = data
        self.success = check_success(data)
        if self.success:
            self.x = data["x"]
            self.y = data["y"]
            self.angle = data["angle"]
            self.confidence = data["confidence"]
            self.current_station = data["current_station"]
            self.last_station = data["last_station"]
            self.create_on = data["create_on"]
        else:
            self.err_msg = data["err_msg"]
            self.create_on = data["create_on"]

        return self.success


class StatusSpeed:

    def __init__(self) -> None:
        self.requestId = 0
        self.messageType = 1005  # robot speed query
        self.msg = {}  # empty message

        # AGV speed attributes
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

        self.success = False
        self.err_msg = ""
        self.create_on = ""

        self.json_data = {}

    def _get_status(self, transport):
        # send command and receive data
        data = transport.send_n_receive(self.requestId, self.messageType,
                                        self.msg)
        # parse data
        self.json_data = data
        self.success = check_success(data)
        if self.success:
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
            self.create_on = data["create_on"]
        else:
            self.err_msg = data["err_msg"]
            self.create_on = data["create_on"]
        return self.success


class StatusForklift:

    def __init__(self) -> None:
        """Get the fork status of the AGV and the current fork height including the fork height in place and the fork auto flag.
        To inspect all the values, you can use "json_data" attribute.
        """
        self.requestId = 0
        self.messageType = 1028  # forklift status query
        self.msg = {}  # empty message

        # forklift status attributes
        self.fork_height = 0
        self.fork_height_in_place = False
        self.fork_auto_flag = False
        self.forward_val = 0
        self.forward_in_place = False
        self.fork_pressure_actual = 0

        self.success = False
        self.err_msg = ""
        self.create_on = ""

        self.json_data = {}

    def _get_status(self, transport):
        # send command and receive data
        transport.send_command(self.requestId, self.messageType, self.msg)
        data = transport.listen()
        # parse data
        self.json_data = data
        self.success = check_success(data)
        if self.success:
            self.fork_height = data["fork_height"]
            self.fork_height_in_place = data["fork_height_in_place"]
            self.fork_auto_flag = data["fork_auto_flag"]
            self.forward_val = data["forward_val"]
            self.forward_in_place = data["forward_in_place"]
            self.fork_pressure_actual = data["fork_pressure_actual"]
            self.create_on = data["create_on"]

        else:
            self.err_msg = data["err_msg"]
            self.create_on = data["create_on"]
        return self.success


class StatusBlocked:

    def __init__(self) -> None:
        """
        Get the status of why the AGV is blocked and the current slow down status.
        """
        self.requestId = 0
        self.messageType = 1006  # blocked status query
        self.msg = {}  # empty message

        self.blocked = False
        self.block_reason = ""
        self.block_x = 0
        self.block_y = 0
        self.block_id = 0
        self.slow_down = False
        self.slow_reason = ""
        self.slow_x = 0
        self.slow_y = 0
        self.slow_id = 0

        self.success = False
        self.err_msg = ""
        self.create_on = ""

        self.json_data = {}

    @staticmethod
    def translate_reason(reason_id):
        if reason_id == 0:
            return "Utrasonic sensor"
        elif reason_id == 1:
            return "Laser sensor"
        elif reason_id == 2:
            return "Falling Down"
        elif reason_id == 3:
            return "Collision"
        elif reason_id == 4:
            return "Infrared sensor"
        elif reason_id == 5:
            return "Lock Switch"
        elif reason_id == 6:
            return "Dynamic Obstacle"
        elif reason_id == 7:
            return "Virtual Wall"
        elif reason_id == 8:
            return "3D Camera"
        elif reason_id == 9:
            return "Distance Sensor"
        elif reason_id == 10:
            return "DI Ultrasond"
        else:
            return "Unknown"

    def _get_status(self, transport):
        self.live = False
        # send command and receive data
        data = transport.send_n_receive(self.requestId, self.messageType,
                                        self.msg)
        # parse data
        self.json_data = data
        self.success = check_success(data)
        if self.success:
            self.blocked = data["blocked"]
            self.block_reason = self.translate_reason(data["block_reason"])
            self.block_x = data["block_x"]
            self.block_y = data["block_y"]
            self.block_id = data["block_id"]
            self.slow_down = data["slow_down"]
            self.slow_reason = self.translate_reason(data["slow_reason"])
            self.slow_x = data["slow_x"]
            self.slow_y = data["slow_y"]
            self.slow_id = data["slow_id"]
            self.create_on = data["create_on"]
        else:
            self.err_msg = data["err_msg"]
            self.create_on = data["create_on"]
        return self.success


class StatusLaserData:

    def __init__(self) -> None:
        """
        Get the laser data of the AGV.
        """
        self.requestId = 0
        self.messageType = 1009  # laser point data query
        self.msg = {}  # empty message

        self.lasers = []

        self.success = False
        self.err_msg = ""
        self.create_on = ""

        self.json_data = {}

    def _get_status(self, transport):
        self.live = False
        # send command and receive data
        data = transport.send_n_receive(self.requestId, self.messageType,
                                        self.msg)
        # parse data
        self.json_data = data
        self.success = check_success(data)
        if self.success:
            self.lasers = data["lasers"]
            self.create_on = data["create_on"]
        else:
            self.err_msg = data["err_msg"]
            self.create_on = data["create_on"]
        return self.success


class StatusEmergencyStop:

    def __init__(self) -> None:
        """Emergency stop status query"""
        self.requestId = 0
        self.messageType = 1012  # emergency stop request
        self.msg = {}  # empty message

        # attributes
        self.emergency = False
        self.driver_emc = False
        self.electric = False
        self.soft_emc = False

        self.success = False
        self.err_msg = ""
        self.create_on = ""

        self.json_data = {}

    def _get_status(self, transport):
        self.live = False
        # send command and receive data
        data = transport.send_n_receive(self.requestId, self.messageType,
                                        self.msg)
        # parse data
        self.json_data = data
        self.success = check_success(data)
        if self.success:
            self.emergency = data["emergency"]
            self.driver_emc = data["driver_emc"]
            self.electric = data["electric"]
            self.soft_emc = data["soft_emc"]
            self.create_on = data["create_on"]
        else:
            self.err_msg = data["err_msg"]
            self.create_on = data["create_on"]
        return self.success


class StatusNavigation:

    def __init__(self) -> None:
        """Navigation status query"""
        self.requestId = 0
        self.messageType = 1020  # navigation status query
        self.msg = {}  # empty message

        # attributes
        self.task_status = ""
        self.task_type = ""
        self.target_id = ""
        self.target_point = None
        self.finished_path = None
        self.unfinished_path = None
        self.move_status = ""

        self.success = False
        self.err_msg = ""
        self.create_on = ""

        self.json_data = {}

    @staticmethod
    def translate_task_status(status_id):
        if status_id == 0:
            return "None"
        elif status_id == 1:
            return "Waiting"
        elif status_id == 2:
            return "Running"
        elif status_id == 3:
            return "Suspended"
        elif status_id == 4:
            return "Completed"
        elif status_id == 5:
            return "Failed"
        elif status_id == 6:
            return "Canceled"
        else:
            return "Unknown"

    @staticmethod
    def translate_task_type(type_id):
        if type_id == 0:
            return "None"
        elif type_id == 1:
            return "Free Navigation to Point"
        elif type_id == 2:
            return "Free Navigation to Station"
        elif type_id == 3:
            return "Path Navigation to Station"
        elif type_id == 4:
            return "Inspection Navigation"
        elif type_id == 7:
            return "Translational rotation"
        elif type_id == 100:
            return "Other"
        else:
            return "Unknown"

    def _get_status(self, transport):
        data = transport.send_n_receive(self.requestId, self.messageType,
                                        self.msg)

        self.json_data = data
        self.success = check_success(data)
        if self.success:
            self.task_status = self.translate_task_status(data["task_status"])
            self.task_type = self.translate_task_type(data["task_type"])
            self.target_id = data["target_id"]
            self.target_point = data["target_point"]
            self.finished_path = data["finished_path"]
            self.unfinished_path = data["unfinished_path"]
            self.create_on = data["create_on"]
        else:
            self.err_msg = data["err_msg"]
            self.create_on = data["create_on"]
        return self.success


class StatusAPI:

    def __init__(self, ip: str, port: int = API_PORT_STATE) -> None:
        """
        Initialize the AGV STATE API class. This connects to the AGV STATE PORT and exchanges status messages with AGV.
        
        Usage:
        ```python
        battery_status = StatusBattery()
        agv_pose = StatusPose()
        
        status = StatusAPI("127.0.0.1")
        status.get_status(battery_status)
        status.get_status(agv_pose)
        print(battery_status.voltage)
        print(battery_status.current)
        print(agv_pose.x)
        print(agv_pose.y)
        
        Args:
            ip (str): AGV ip address
            port (int, optional): port at which AGV STATE API is implemented . Defaults to API_PORT_STATE.
        """
        self.ip = ip
        self.port = port
        self.transport = TcpTransport(ip, port)
        self.connected = False
        self.connected = self.transport.connected

    def get_status(self, status):
        """exchange status with AGV for the status class like BatteryStatus, NavigationStatus etc.
        """
        return status._get_status(self.transport)
