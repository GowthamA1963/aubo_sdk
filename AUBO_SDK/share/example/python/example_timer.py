#! /usr/bin/env python
# coding=utf-8

"""
Test timer functions: start, stop, reset, delete

Steps:
Step 1: Connect to RPC service and login to the robot
Step 2: Example 1
    1. Start timer1, wait 7.5s, stop timer1, get duration (about 7.5s)
    2. Repeat above, get duration (about 15.0s)
    3. Reset timer1, get duration (about 0.0s), delete timer1
Step 3: Example 2
    1. Start timer1, wait 7.5s, get duration (about 7.5s), reset timer1
    2. Start timer1, wait 7.5s, get duration (about 7.5s), reset and delete timer1
"""

import time
import pyaubo_sdk

robot_ip = "127.0.0.1"  # Server IP address
robot_port = 30004      # Port number
M_PI = 3.14159265358979323846
robot_rpc_client = pyaubo_sdk.RpcClient()

if __name__ == '__main__':
    robot_rpc_client.connect(robot_ip, robot_port)  # Connect to RPC service
    if robot_rpc_client.hasConnected():
        print("Robot rpc_client connected successfully!")
        robot_rpc_client.login("aubo", "123456")  # Login to robot
        if robot_rpc_client.hasLogined():
            print("Robot rpc_client logged in successfully!")
            robot_name = robot_rpc_client.getRobotNames()[0]  # Get robot name
            impl = robot_rpc_client.getRobotInterface(robot_name)

            print("Example 1 ---------------")
            # Start timer1, wait 7.5s, stop timer1, get duration (about 7.5s)
            robot_rpc_client.getRuntimeMachine().timerStart("timer1")
            time.sleep(7.5)
            robot_rpc_client.getRuntimeMachine().timerStop("timer1")
            timer1 = robot_rpc_client.getRuntimeMachine().getTimer("timer1")
            print("Duration = ", timer1)

            # Start timer1, wait 7.5s, stop timer1, get duration (about 15.0s)
            robot_rpc_client.getRuntimeMachine().timerStart("timer1")
            time.sleep(7.5)
            robot_rpc_client.getRuntimeMachine().timerStop("timer1")
            timer1 = robot_rpc_client.getRuntimeMachine().getTimer("timer1")
            print("Duration = ", timer1)

            # Reset timer1, get duration (about 0.0s), delete timer1
            robot_rpc_client.getRuntimeMachine().timerReset("timer1")
            timer1 = robot_rpc_client.getRuntimeMachine().getTimer("timer1")
            print("Duration = ", timer1)
            robot_rpc_client.getRuntimeMachine().timerDelete("timer1")

            print("Example 2 ---------------")
            # Start timer1, wait 7.5s, get duration (about 7.5s), reset timer1
            robot_rpc_client.getRuntimeMachine().timerStart("timer1")
            time.sleep(7.5)
            timer1 = robot_rpc_client.getRuntimeMachine().getTimer("timer1")
            print("Duration = ", timer1)
            robot_rpc_client.getRuntimeMachine().timerReset("timer1")

            # Start timer1, wait 7.5s, get duration (about 7.5s), reset and delete timer1
            robot_rpc_client.getRuntimeMachine().timerStart("timer1")
            time.sleep(7.5)
            timer1 = robot_rpc_client.getRuntimeMachine().getTimer("timer1")
            print("Duration = ", timer1)
            robot_rpc_client.getRuntimeMachine().timerReset("timer1")
            robot_rpc_client.getRuntimeMachine().timerDelete("timer1")
