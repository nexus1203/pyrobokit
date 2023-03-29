# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║ File:           utils.py                                 ║
║ Author:         Nexus1203                                ║
║ Created:        2023-03-29                               ║
║ Last Modified:  2023-03-29                               ║
║ Description:    Utility code for AGV API                 ║  
╚══════════════════════════════════════════════════════════╝
"""


def check_success(response):
    if response['ret_code'] != 0:
        print("Error: ", response['ret_code'])
        return False
    else:
        return True


def to_json(class_instance):
    as_json = class_instance.__dict__
    # remove None values
    as_json = {k: v for k, v in as_json.items() if v is not None}
    # remove request id, message type and msg if they exist
    as_json.pop("requestId", None)
    as_json.pop("messageType", None)
    as_json.pop("msg", None)

    return as_json