# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║ File:           transport.py                             ║
║ Author:         Nexus1203                                ║
║ Created:        2023-03-23                               ║
║ Last Modified:  2023-03-23                               ║
║ Description:    TCP/IP client with reconnect features,   ║
║                 and a encoding decoding for robotkit     ║
║                  interface.                              ║  
╚══════════════════════════════════════════════════════════╝
"""

import socket
import struct
import json
import time
from datetime import datetime


class SeerData:

    def __init__(self):
        self.header = bytearray(
            struct.pack('!BBHLH6s', 0x5A, 0x01, 0, 0, 0,
                        b'\x00\x00\x00\x00\x00\x00'))
        self.data = bytearray()

    def size(self):
        _, _, _, _, m_length = struct.unpack('!BBHLH6s', self.header)
        return 16 + m_length

    def set_data(self, msg_type, msg=None, request_id=0):
        if msg:
            as_json = json.dumps(msg)
            data = bytearray(as_json, 'ascii')
            size = len(data)
        else:
            data = bytearray()
            size = 0

        self.header = bytearray(
            struct.pack('!BBHLH6s', 0x5A, 0x01, request_id, size, msg_type,
                        b'\x00\x00\x00\x00\x00\x00'))
        self.data = data

        return 16 + size

    def get_packed_message(self):
        return self.header + self.data


def unpack_header(data):
    PACK_HEAD_FMT_STR = '!BBHLH6s'
    result = struct.unpack(PACK_HEAD_FMT_STR, data)
    jsonLen = result[3]
    reqNum = result[4]

    return (jsonLen, reqNum)


class TcpTransport:

    def __init__(self, ip, port):
        self.name = "TCP Transport"
        self.ip = ip
        self.port = port
        self.connected = False
        self.socket = None
        self.connect()

    def connect(self):
        i = 0
        while not self.connected:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.setblocking(True)
                self.socket.connect((self.ip, self.port))
                self.connected = True
            except socket.error as e:
                print(f"Connection error: {e}. Retrying...")
                time.sleep(5)
                i += 1
                if i > 10:
                    print("Unable to connect. Exiting.")
                    break

    def disconnect(self):
        self.connected = False
        self.socket.close()

    def listen(self):
        data = None
        try:
            header = self.socket.recv(16)
            print(header)
            jsonLen, reqNum = unpack_header(header)

            data = self.socket.recv(jsonLen + 1)
            data = data.decode('utf-8')
            data = json.loads(data)

        except Exception as e:
            print(f"Error: {e}")

        if data:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            log = (f"[{timestamp}] [{self.name}] :: Received: {data}")
            if jsonLen > 0 and jsonLen < 1000:
                print(log)
            data['timestamp'] = timestamp
        return data

    def send(self, message):
        if self.connected:
            try:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S",
                                          time.localtime())
                print(message.hex())
                self.socket.sendall(message)
                log = (f"[{timestamp}] [{self.name}] :: Sent: {message}")
                print(log)
                # print(f"[{timestamp}] Sent: {message}")
            except socket.error as e:
                self.disconnect()
                self.connect()
        else:
            print("Not connected. Unable to send message.")

    def send_command(self, requestID, messageType, data={}):
        # message = pack_message(requestID, messageType, data)
        s = SeerData()
        s.set_data(request_id=requestID,
                   msg_type=messageType,
                   msg=None if {} else data)
        message = s.get_packed_message()
        self.send(message)

    def send_n_receive(self, requestID, messageType, data={}):
        self.send_command(requestID, messageType, data)
        # time.sleep(0.01)
        return self.listen()


if __name__ == "__main__":
    transport = TcpTransport("127.0.0.1", 12345)

    while True:
        message = input("Enter message to send: ")
        transport.send(message)
        transport.listen()
