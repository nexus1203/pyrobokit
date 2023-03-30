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

    def __init__(self, ListDigitalOutput: list = None):
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

    def __init__(self, height: float = 0.0):
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


class AudioList:

    def __init__(self) -> None:
        """Get a list of available audio files"""
        self.requestId = 0
        self.messageType = 6033
        self.msg = {}
        self.audio_list = []

    def execute(self, transport):
        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        if check_success(response):
            self.audio_list = response["audios"]
            return True
        else:
            return False


class AudioPlay:

    def __init__(self, name: str, loop: bool = False) -> None:
        """
        A class to play audio

        Args:
            name (str): filename of the audio file
            loop (bool, optional): loop the audio. Defaults to False.
        """
        self.requestId = 0
        self.messageType = 6000
        self.msg = {}
        if name is None:
            raise ValueError(
                "Audio name cannot be None, please provide a valid name\n." +
                "You can get a list of available audio files with the AudioList class"
            )
        self.name = name
        self.loop = loop

    def execute(self, transport):
        self.msg = to_json(self)
        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class AudioPause:

    def __init__(self) -> None:
        """Pause playing audio"""
        self.requestId = 0
        self.messageType = 6010
        self.msg = {}

    def execute(self, transport):
        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class AudioContine:

    def __init__(self) -> None:
        """Continue playing audio"""
        self.requestId = 0
        self.messageType = 6011
        self.msg = {}

    def execute(self, transport):
        response = transport.send_n_receive(self.requestId, self.messageType,
                                            self.msg)
        return check_success(response)


class AudioStop:

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


class OtherAPI:

    def __init__(self, ip: str, port: int = API_PORT_OTHER):
        """Other API class. This class is used to execute other API requests.
        
        usage:
        ```python
        oapi = OtherAPI("127.0.0.1")
        # set digital output 0 to True
        success = oapi.execute(SetDigitalOutput(0, True))
        # set forklift height to 0.05 m
        success = oapi.execute(ForkliftHeight(0.05))
        # soft stop the forklift
        success = oapi.execute(SoftEMC(stop=True))
        
        # get the list of available audio files
        audio_list = AudioList()
        success = oapi.execute(audio_list)
        print(audio_list.audio_list)
        ```
        
        Args:
            ip (str): IP address of the AGV's SEER controller
            port (int, optional): API port of Other functions. Defaults to API_PORT_OTHER.
        """
        self.ip = ip
        self.port = port
        self.transport = TcpTransport(ip, port)

    def execute(self, request):
        """execute a request and return the response

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        return request.execute(self.transport)
