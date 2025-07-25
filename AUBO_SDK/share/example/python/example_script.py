#! /usr/bin/env python
# coding=utf-8

"""
Run Script

Steps:
Step 1: Connect to the RPC service and log in to the robot arm
Step 2: Connect to the SCRIPT service and log in to the robot arm
Step 3: Run the script
Step 4: When the planner stops running, stop the script
"""
import time

import pyaubo_sdk

robot_ip = "192.168.0.141"  # Server IP address
M_PI = 3.14159265358979323846
robot_rpc_client = pyaubo_sdk.RpcClient()
robot_script_client = pyaubo_sdk.ScriptClient()


def exampleScript():
    robot_script_client.sendFile(r"D:\AUBO_SDK\AUBO_SDK\share\example\aubo_script\example_movej.lua")
    pass


if __name__ == '__main__':
    robot_rpc_client.connect(robot_ip, 30004)  # Connect to RPC service
    robot_rpc_client.setRequestTimeout(10)
    if robot_rpc_client.hasConnected():
        print("Robot rpc_client connected successfully!")
    robot_rpc_client.login("aubo", "123456")  # Robot arm login
    robot_script_client.connect(robot_ip, 30002)  # Connect to SCRIPT service
    robot_script_client.login("aubo", "123456")  # Robot arm login

    exampleScript()  # Run script

    while True:
        time.sleep(1)
        runtime_state = robot_rpc_client.getRuntimeMachine().getStatus()
        if runtime_state != pyaubo_sdk.RuntimeState.Running:  # When planner stops, stop script
            print("Planner state:", runtime_state)
            break
        print("Planner state:", runtime_state)