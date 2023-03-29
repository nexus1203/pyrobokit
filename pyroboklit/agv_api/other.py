# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║ File:           other.py                                 ║
║ Author:         Nexus1203                                ║
║ Created:        2023-03-29                               ║
║ Last Modified:  2023-03-29                               ║
║ Description:    Other functions port of robotkit api     ║  
╚══════════════════════════════════════════════════════════╝
"""

from ..tcp_transport import TcpTransport
from ..tcp_transport import API_PORT_OTHER
from .utils import check_success, to_json


class SoftEMC:

    def __init__(self, stop: bool = True):
        """
        A class to control the software emergency stop of the robotkit API

        Args:
            stop (bool, optional): set the software emergency to True or false. Defaults to True.
        """
        self.requestId = 0
        self.messageType = 6004  # softEMC
        self.msg = {}

        self.status = stop

    def execute(self, transport):
        self.msg = to_json(self)

        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class SetDigitalInput:

    def __init__(self, id: int, value: bool = False):
        """
        A class to set the value of a digital input virtually

        Args:
            id (int): id of the digital input
            value (bool): value to set, True or False. Defaults to False.
        """
        self.requestId = 0
        self.messageType = 6020
        self.msg = {}
        self.id = id
        self.status = value

    def execute(self, transport):
        self.msg = to_json(self)

        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class SetDigitalOutput:

    def __init__(self, id: int, value: bool = False):
        """
        A class to set the value of a digital output virtually

        Args:
            id (int): id of the digital output
            value (bool): value to set, True or False. Defaults to False.
        """
        self.requestId = 0
        self.messageType = 6001
        self.msg = {}
        self.id = id
        self.status = value

    def execute(self, transport):
        self.msg = to_json(self)

        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class SetBatchDigitalOutput:

    def __init__(self, ListDigitalOutput: list):
        """
        A class to set the value of a digital output virtually

        Args:
            ListDigitalOutput (list): list of digital output class ([SetDigitalOutput(0, True), SetDigitalOutput(1, False)])
        """
        self.requestId = 0
        self.messageType = 6002
        self.msg = {}
        self.IO_list = ListDigitalOutput

    def execute(self, transport):
        as_json = [to_json(io_class) for io_class in self.IO_list]

        response = transport.send_n_receive(self.requestId, self.messageType,
                                            as_json)
        return check_success(response)


class ForkliftStop:

    def __init__(self):
        """
        A class to stop the forklift
        """
        self.requestId = 0
        self.messageType = 6041
        self.msg = {}

    def execute(self, transport):
        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class ForkliftHeight:

    def __init__(self, height: float):
        """
        A class to set the forklift height

        Args:
            height (float): height to set
        """
        self.requestId = 0
        self.messageType = 6040
        self.msg = {}
        self.height = height

    def execute(self, transport):
        self.msg = to_json(self)

        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class StopAudio:

    def __init__(self) -> None:
        """
        A class to stop the audio
        """
        self.requestId = 0
        self.messageType = 6012
        self.msg = {}

    def execute(self, transport):
        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)
