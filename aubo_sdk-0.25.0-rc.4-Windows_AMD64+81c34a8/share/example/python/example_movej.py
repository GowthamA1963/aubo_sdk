#! /usr/bin/env python
# coding=utf-8

"""
Function: Joint motion of the robotic arm

Steps:
Step 1: Set RPC timeout, connect to RPC server, login to the robot
Step 2: Set movement speed ratio, and pass through 3 waypoints using joint motion
Step 3: Logout and disconnect from RPC
"""

import time
import math
import pyaubo_sdk

robot_ip = "192.168.0.141"  # Robot IP address
robot_port = 30004          # Port number

# Blocking function to wait for motion completion
def wait_arrival(robot_interface):
    max_retry_count = 5
    cnt = 0

    # Call API: Get the current motion command ID
    exec_id = robot_interface.getMotionControl().getExecId()

    # Wait for the robot to start moving
    while exec_id == -1:
        if cnt > max_retry_count:
            return -1
        time.sleep(0.05)
        cnt += 1
        exec_id = robot_interface.getMotionControl().getExecId()

    # Wait for the robot to finish moving
    while robot_interface.getMotionControl().getExecId() != -1:
        time.sleep(0.05)

    return 0

# Pass through 3 waypoints using joint motion
def example_movej(rpc_client):
    # Joint angles in radians
    q1 = [0.0 * (math.pi / 180), -15.0 * (math.pi / 180), 100.0 * (math.pi / 180),
          25.0 * (math.pi / 180), 90.0 * (math.pi / 180), 0.0 * (math.pi / 180)
          ]
    q2 = [35.92 * (math.pi / 180), -11.28 * (math.pi / 180), 59.96 * (math.pi / 180),
          -18.76 * (math.pi / 180), 90.0 * (math.pi / 180), 35.92 * (math.pi / 180)
          ]
    q3 = [41.04 * (math.pi / 180), -7.65 * (math.pi / 180), 98.80 * (math.pi / 180),
          16.44 * (math.pi / 180), 90.0 * (math.pi / 180), 11.64 * (math.pi / 180)
          ]

    # Call API: Get the robot's name
    robot_name = rpc_client.getRobotNames()[0]
    robot_interface = rpc_client.getRobotInterface(robot_name)

    # Call API: Set the robot’s speed ratio
    robot_interface.getMotionControl().setSpeedFraction(0.30)

    # Move to waypoint q1
    robot_interface.getMotionControl() \
        .moveJoint(q1, 80 * (math.pi / 180), 60 * (math.pi / 180), 0, 0)

    # Wait for completion
    ret = wait_arrival(robot_interface)
    if ret == 0:
        print("Joint motion to waypoint 1 succeeded")
    else:
        print("Joint motion to waypoint 1 failed")

    # Move to waypoint q2
    robot_interface.getMotionControl() \
        .moveJoint(q2, 80 * (math.pi / 180), 60 * (math.pi / 180), 0, 0)

    # Wait for completion
    ret = wait_arrival(robot_interface)
    if ret == 0:
        print("Joint motion to waypoint 2 succeeded")
    else:
        print("Joint motion to waypoint 2 failed")

    # Move to waypoint q3
    robot_interface.getMotionControl() \
        .moveJoint(q3, 80 * (math.pi / 180), 60 * (math.pi / 180), 0, 0)

    # Wait for completion
    ret = wait_arrival(robot_interface)
    if ret == 0:
        print("Joint motion to waypoint 3 succeeded")
    else:
        print("Joint motion to waypoint 3 failed")


if __name__ == '__main__':
    robot_rpc_client = pyaubo_sdk.RpcClient()
    robot_rpc_client.setRequestTimeout(1000)  # Call API: Set RPC timeout
    robot_rpc_client.connect(robot_ip, robot_port)  # Call API: Connect to RPC server
    if robot_rpc_client.hasConnected():
        print("RPC client connected successfully!")
        robot_rpc_client.login("aubo", "123456")  # Call API: Login
        if robot_rpc_client.hasLogined():
            print("RPC client logged in successfully!")
            example_movej(robot_rpc_client)  # Perform joint motion through waypoints
            robot_rpc_client.logout()  # Logout
            robot_rpc_client.disconnect()  # Disconnect
