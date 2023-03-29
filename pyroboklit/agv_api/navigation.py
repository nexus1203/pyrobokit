# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║ File:           navigation.py                            ║
║ Author:         Nexus1203                                ║
║ Created:        2023-03-28                               ║
║ Last Modified:  2023-03-28                               ║
║ Description:    Navigation port features of robotkit api ║  
╚══════════════════════════════════════════════════════════╝
"""

from ..tcp_transport import TcpTransport
from ..tcp_transport import API_PORT_TASK
from .utils import check_success
# import time


class TaskOneStation:

    def __init__(self, dest_id: str, source_id: str, task_id: str,
                 angle: float, method: str, max_speed: float,
                 max_wspeed: float, max_acc: float, max_wacc: float,
                 duration: float, orientation: float, spin: bool) -> None:
        """
        Single Station Task. The AGV will move to the target site and stop there.
        One may repeat send a single station tasks to the AGV in order to set its maximum speed, acceleration, and angular speed.
        
        usage:
        ```python
        from time import sleep
        # create a task object
        task = TaskOneStation(dest_id="LM15", source_id = "LM1", max_speed=0.5)
        # use the Navigation class to send the task to the AGV
        Nav = Navigation(ip = "127.0.0.1")
        Nav.execute(task)
        # wait for 5 seconds
        sleep(5)
        # change the speed to 0.2 m/s
        task.max_speed = 0.2
        success = Nav.execute(task)
        print(success)
        ```        
        
        Args:
            dest_id (str): destination id must be set as string (e.g. "LM15", "AP14")
            source_id (str): source id is optional but should be set as string (e.g. "LM15", "AP14")
            task_id (str): task number is optional as string (e.g. "82444872")
            angle (float): The angle value at the target site. The angle is optional and is given in degrees. 
                        The angle is measured from the x-axis of the map. The angle is measured clockwise. 
            method (str): the movement method can only be "forward" or "backward". It defines how the AGV ill approach the target.
            max_speed (float): maximum speed in m/s
            max_wspeed (float): maximum angular speed in rad/s
            max_acc (float): maximum acceleration in m/s^2
            max_wacc (float): maximum angular acceleration in rad/s^2
            duration (float): duration in milliseconds for delaying the end of navigation state
            orientation (float): not used
            spin (bool): Follow up	(repeat the task after completion of the task)
        """
        self.requestId = 0
        self.messageType = 3051  # single point task
        self.msg = {}

        self.id = dest_id  # destination id must be set
        self.source_id = source_id  # source id is optional but should be set
        self.task_id = task_id  # task id is optional
        self.angle = angle  # angle is optional
        self.method = method  # method is optional
        self.max_speed = max_speed  # max speed is optional
        self.max_wspeed = max_wspeed
        self.max_acc = max_acc
        self.max_wacc = max_wacc
        self.duration = duration
        self.orientation = orientation
        self.spin = spin

    def to_json(self) -> str:
        as_json = self.__dict__
        # remove None values
        as_json = {k: v for k, v in as_json.items() if v is not None}

        return as_json

    def execute(self, transport):
        """_summary_

        Args:
            transport (TcpTransport): transport object
        """
        self.msg = self.to_json()
        if "id" not in self.msg:
            raise ValueError(
                "destination id is required, please set the dest_id as string (e.g. 'LM15', 'AP14')"
            )
        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class TaskMultiStation:

    def __init__(self, tasks: list) -> None:
        """
        Move to multiple stations. This is a multi-point task. The AGV will move to the first station, 
        then to the second station, and so on. The AGV will stop at the last station.
        If the duration is not set for the stations in between, the AGV will not stop at these stations and will move directly to the next station.
        In order to stop for a period of time at the stations in between, the duration should be set for these station's tasks in TaskOneStation.
        
        Usage:
        ```python
        # create three station tasks
        task1 = TaskOneStation(dest_id="LM15", source_id = "LM1", duration=100)
        task2 = TaskOneStation(dest_id="LM16", source_id = "LM15", duration=0)
        task3 = TaskOneStation(dest_id="LM17", source_id = "LM16", duration=100)
        # combine the tasks into a multi-point task
        m_task = TaskMultiStation([task1, task2, task3])
        # use the Navigation class to send the task to the AGV
        Nav = Navigation(ip = "127.0.0.1")
        success = Nav.execute(m_task)
        print(success)
        ```
        In above code, the AGV will move from LM1 to LM15, then stop for 100ms, and move to LM16, then move to LM17 without any delay in between, then stop for 100ms.

        Args:
            tasks (list): list of TaskOneStation
        """
        self.requestId = 0
        self.messageType = 3066  # multi point task
        self.msg = {}

        self.tasks = tasks

    def to_json(self) -> str:
        as_json = {"move_task_list": [task.to_json() for task in self.tasks]}
        return as_json

    def execute(self, transport):
        """_summary_

        Args:
            transport (TcpTransport): transport object
        """
        self.msg = self.to_json()
        if "move_task_list" not in self.msg:
            raise ValueError("task list is required")
        if len(self.msg["move_task_list"]) == 0:
            raise ValueError("task list is empty")

        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class TaskCoordinate:

    def __init__(self, x: float, y: float, angle: float, max_speed: float,
                 max_wspeed: float, max_acc: float, max_wacc: float) -> None:
        """
        Move the AGV to a specific coordinate on the map. The AGV will move to the target coordinate and stop.
        if the angle is not set, the AGV will not rotate. If the angle is set, the AGV will rotate to the target angle.
        One should always provide atleast three parameters (x, y, angle) to ensure that the AGV will move to the target coordinate.
        This function should be used with caution as it can lead to collisions if the AGV is not moving in the right direction.

        Args:
            x (float): x coordinate of the target site
            y (float): y coordinate of the target site
            angle (float): The angle value at the target site. The angle is optional and is given in degrees. 
                        The angle is measured from the x-axis of the map. The angle is measured clockwise. 
            max_speed (float): maximum speed in m/s
            max_wspeed (float): maximum angular speed in rad/s
            max_acc (float): maximum acceleration in m/s^2
            max_wacc (float): maximum angular acceleration in rad/s^2
        """
        self.requestId = 0
        self.messageType = 3050  # go to x, y, a coordinate task
        self.msg = {}

        self.x = x
        self.y = y
        self.angle = angle
        self.max_speed = max_speed
        self.max_wspeed = max_wspeed
        self.max_acc = max_acc
        self.max_wacc = max_wacc

    def to_json(self) -> str:
        as_json = self.__dict__
        # remove None values
        as_json = {k: v for k, v in as_json.items() if v is not None}

        return as_json

    def execute(self, transport):
        """_summary_

        Args:
            transport (TcpTransport): transport object
        """
        self.msg = self.to_json()
        if "angle" not in self.msg:
            raise ValueError("angle is required")
        if "x" not in self.msg:
            raise ValueError("x is required")
        if "y" not in self.msg:
            raise ValueError("y is required")
        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class TaskSuspend:

    def __init__(self) -> None:
        """
        Suspend the current task. (can be resumed later using TaskResume)
        """
        self.requestId = 0
        self.messageType = 3001  # suspend task
        self.msg = {}

    def execute(self, transport):
        """_summary_

        Args:
            transport (TcpTransport): transport object
        """
        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class TaskResume:

    def __init__(self) -> None:
        """
        Resume the current task. (only for suspended tasks)
        """
        self.requestId = 0
        self.messageType = 3002  # resume task
        self.msg = {}

    def execute(self, transport):
        """ excute the task

        Args:
            transport (TcpTransport): transport object
        """
        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class TaskCancel:

    def __init__(self) -> None:
        """
        Cancel the current task.
        """
        self.requestId = 0
        self.messageType = 3003  # cancel task
        self.msg = {}

    def execute(self, transport):
        """_summary_

        Args:
            transport (TcpTransport): transport object
        """
        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class Navigation:

    def __init__(self, ip: str, port: int = API_PORT_TASK) -> None:
        """Navigation class.
        An instance of this class is used to manage navigation commands to the robot.

        Args:
            ip (str): _description_
            port (int, optional): _description_. Defaults to API_PORT_TASK.
        """

        self.ip = ip
        self.port = port
        self.transport = TcpTransport(self.ip, self.port)

    def execute(self, task):
        """Excetute a task on the AGV.
        Note that the task is executed in a non-blocking way, so the function will return immediately after the task is sent to the AGV.
        in order to check if the task is finished, refer the Status class of the API.
        usage:
        To move AGV to a specific station on the map:
        ```
        Nav = Navigation(ip='127.0.0.1')
        s_task = TaskOneStation(dest_id='LM15', max_speed=0.5, max_acc=0.5)
        success = Nav.execute(s_task)
        print(success)
        ```
        To cancel the task:
        ```
        Nav = Navigation(ip='127.0.0.1')
        success = Nav.execute(TaskCancel())
        print(success)
        ```
        Args:
            task (Task): Task object to be executed
        """
        return task.execute(self.transport)