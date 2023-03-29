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