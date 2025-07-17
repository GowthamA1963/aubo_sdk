#! /usr/bin/env python
# coding=utf-8

"""
Robot Arm Linear Motion Example

Steps:
1. Set RPC timeout, connect to RPC service, and log in to the robot.
2. Move to the start position with joint motion, then pass through 3 waypoints with linear motion.
3. Log out and disconnect from the RPC service.
"""
import time
import math
import pyaubo_sdk

robot_ip = "192.168.0.141"  # Server IP address
robot_port = 30004       # Port number
robot_rpc_client = pyaubo_sdk.RpcClient()


# Blocking wait until motion is finished
def wait_arrival(robot_interface):
    max_retry_count = 5
    cnt = 0

    # Get the current motion command ID
    exec_id = robot_interface.getMotionControl().getExecId()

    # Wait for the robot arm to start moving
    while exec_id == -1:
        if cnt > max_retry_count:
            return -1
        time.sleep(0.05)
        cnt += 1
        exec_id = robot_interface.getMotionControl().getExecId()

    # Wait for the robot arm to finish moving
    while robot_interface.getMotionControl().getExecId() != -1:
        time.sleep(0.05)

    return 0


# Move to the start position with joint motion, then pass through 3 waypoints with linear motion
def example_movel(rpc_client):
    # Waypoint in joint angles (radians)
    q = [0.0 * (math.pi / 180), -15.0 * (math.pi / 180), 100.0 * (math.pi / 180), 25.0 * (math.pi / 180),
         90.0 * (math.pi / 180), 0.0 * (math.pi / 180)]
    # Waypoints in pose [x, y, z, rx, ry, rz], position in meters, orientation in radians
    pose1 = [0.551, -0.124, 0.419, -3.134, 0.004, 1.567]
    pose2 = [0.552, 0.235, 0.419, -3.138, 0.007, 1.567]
    pose3 = [0.551, -0.124, 0.261, -3.134, 0.0042, 1.569]

    # Get the robot's name
    robot_name = rpc_client.getRobotNames()[0]

    robot_interface = rpc_client.getRobotInterface(robot_name)

    # Set the robot arm speed ratio
    robot_interface.getMotionControl().setSpeedFraction(0.75)

    # Set the tool center point (TCP offset relative to the flange center)
    tcp_offset = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    robot_interface.getRobotConfig().setTcpOffset(tcp_offset)

    # Move to the initial position with joint motion
    robot_interface.getMotionControl() \
        .moveJoint(q, 80 * (math.pi / 180), 60 * (math.pi / 180), 0, 0)

    # Blocking wait
    ret = wait_arrival(robot_interface)
    if ret == 0:
        print("Joint motion to initial position succeeded")
    else:
        print("Joint motion to initial position failed")

    # Move through 3 waypoints with linear motion
    # Linear motion to waypoint 1
    robot_interface.getMotionControl() \
        .moveLine(pose1, 1.2, 0.25, 0, 0)

    ret = wait_arrival(robot_interface)
    if ret == 0:
        print("Linear motion to waypoint 1 succeeded")
    else:
        print("Linear motion to waypoint 1 failed")

    # Linear motion to waypoint 2
    robot_interface.getMotionControl() \
        .moveLine(pose2, 1.2, 0.25, 0, 0)

    ret = wait_arrival(robot_interface)
    if ret == 0:
        print("Linear motion to waypoint 2 succeeded")
    else:
        print("Linear motion to waypoint 2 failed")

    # Linear motion to waypoint 3
    robot_interface.getMotionControl() \
        .moveLine(pose3, 1.2, 0.25, 0, 0)

    ret = wait_arrival(robot_interface)
    if ret == 0:
        print("Linear motion to waypoint 3 succeeded")
    else:
        print("Linear motion to waypoint 3 failed")


if __name__ == '__main__':
    robot_rpc_client = pyaubo_sdk.RpcClient()
    robot_rpc_client.setRequestTimeout(1000)  # Set RPC timeout
    robot_rpc_client.connect(robot_ip, robot_port)  # Connect to RPC service
    if robot_rpc_client.hasConnected():
        print("RPC client connected successfully!")
        robot_rpc_client.login("aubo", "123456")  # Log in
        example_movel(robot_rpc_client)  # Move to start position, then pass through 3 waypoints with linear motion
        robot_rpc_client.logout()  # Log out
        robot_rpc_client.disconnect()  # Disconnect
    else:
        print("RPC client connection failed!")
