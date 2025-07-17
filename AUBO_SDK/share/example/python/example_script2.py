#! /usr/bin/env python
# coding=utf-8

"""
Run Script

Steps:
Step 1: Connect to the RPC service and log in to the robot arm
Step 2: Connect to the SCRIPT service and log in to the robot arm
Step 3: Enter the script file name
Step 4: Open and read the script file
Step 5: Send the script content
Step 6: When the planner stops running, stop the script execution
"""
import time

import pyaubo_sdk
import os
import sys

robot_ip = "192.168.0.141"  # Server IP address
M_PI = 3.14159265358979323846
robot_rpc_client = pyaubo_sdk.RpcClient()
robot_script_client = pyaubo_sdk.ScriptClient()


if __name__ == '__main__':
    robot_rpc_client.connect(robot_ip, 30004)  # Connect to RPC service
    robot_rpc_client.setRequestTimeout(10)
    if robot_rpc_client.hasConnected():
        print("Robot rpc_client connected successfully!")
    robot_rpc_client.login("aubo", "123456")  # Robot arm login
    robot_script_client.connect(robot_ip, 30002)  # Connect to SCRIPT service
    robot_script_client.login("aubo", "123456")  # Robot arm login

    # Enter script file name
    filename = input("Please enter the file name: ")
    if not os.path.exists(filename):
        print("File does not exist!")
        sys.exit(1)

    # Open and read the script file
    file = open(filename)
    str_all = ""
    for line in file:
        str_all += line
    str_all += "\r\n\r\n"
    print("Script content: \n", str_all)
    file.close()

    # Send the script content
    robot_script_client.sendString(str_all)

    # When the planner stops running, stop the script execution
    while True:
        time.sleep(1)
        runtime_state = robot_rpc_client.getRuntimeMachine().getStatus()
        if runtime_state != pyaubo_sdk.RuntimeState.Running:
            print("Planner state:", runtime_state)
            break
        print("Planner state:", runtime_state)
