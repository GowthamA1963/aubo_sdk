#! /usr/bin/env python
# coding=utf-8

"""
Robot Power On and Power Off

Steps:
Step 1: Connect to the RPC service
Step 2: Robot login
Step 3: Robot power on
Step 4: Robot power off
"""

import pyaubo_sdk
import time

robot_ip = "192.168.0.141"  # Server IP address
robot_port = 30004  # Port number
M_PI = 3.14159265358979323846
robot_rpc_client = pyaubo_sdk.RpcClient()

# Robot power on
def exampleStartup():
    robot_name = robot_rpc_client.getRobotNames()[0]  # Get robot name
    if 0 == robot_rpc_client.getRobotInterface(
            robot_name).getRobotManage().poweron():  # Request robot power on
        print("The robot is requesting power-on!")
        if 0 == robot_rpc_client.getRobotInterface(
                robot_name).getRobotManage().startup():  # Request robot startup
            print("The robot is requesting startup!")
            # Loop until the robot releases the brake successfully
            while 1:
                robot_mode = robot_rpc_client.getRobotInterface(robot_name) \
                    .getRobotState().getRobotModeType()  # Get robot mode type
                print("Robot current mode: %s" % (robot_mode.name))
                if robot_mode == pyaubo_sdk.RobotModeType.Running:
                    break
                time.sleep(1)

# Robot power off
def examplePoweroff():
    robot_name = robot_rpc_client.getRobotNames()[0]  # Get robot name
    if 0 == robot_rpc_client.getRobotInterface(
            robot_name).getRobotManage().poweroff(): # Request robot power off
        print("The robot is requesting power-off!")

if __name__ == '__main__':
    robot_rpc_client.connect(robot_ip, robot_port)  # Connect to RPC service
    if robot_rpc_client.hasConnected():
        print("Robot rpc_client connected successfully!")
        robot_rpc_client.login("aubo", "123456")  # Robot login
        if robot_rpc_client.hasLogined():
            print("Robot rpc_client logged in successfully!")
            exampleStartup()  # Robot power on
            examplePoweroff()  # Robot power off
