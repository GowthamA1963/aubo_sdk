#!/usr/bin/env python
# coding=utf-8

"""
Move the robot arm linearly to a singularity position,
and print the error popup messages from the teach pendant (subscribed via RTDE) to the console.

Steps:
1. Connect and login to the RPC service
2. Connect and login to the RTDE service
3. Set RTDE subscription topic
4. Subscribe to the topic, get log level, error code, and error message
5. Move linearly to a singularity point
"""

import os
import sys
import time
import pyaubo_sdk

robot_ip = "192.168.0.141"
rpc_port = 30004
rtde_port = 30010
M_PI = 3.141592653589793

# Print log level, error code, and message to console
def printlog(level, source, code, content):
    level_names = ["Critical", "Error", "Warning", "Info", "Debug", "BackTrace"]
    sys.stderr.write(f"[{level_names[level.value]}] {source} - {code} {content}\n")

# Subscription callback for RTDE
def subscribe_callback(parser):
    msgs = parser.popRobotMsgVector()
    for msg in msgs:
        error_content = pyaubo_sdk.errorCode2Str(msg.code)
        for arg in msg.args:
            pos = error_content.find("{}")
            if pos != -1:
                error_content = error_content[:pos] + arg + error_content[pos+2:]
            else:
                break
        printlog(msg.level, msg.source, msg.code, error_content)

# Blocking wait for motion completion
def waitArrival(robot_interface):
    while robot_interface.getMotionControl().getExecId() == -1:
        time.sleep(0.1)

    current_id = robot_interface.getMotionControl().getExecId()
    while robot_interface.getMotionControl().getExecId() == current_id:
        time.sleep(0.1)

# Move to a singularity pose
def movel_singularity(robot_interface):
    waypoint_1_q = [-2.40194, 0.103747, 1.7804, 0.108636, 1.57129, -2.6379]
    waypoint_2_p = [1000, 1000, 1000, 3.05165, 0.0324355, 1.80417]

    print("▶️ Moving to joint pose...")
    robot_interface.getMotionControl().moveJoint(
    waypoint_1_q,
    180 * (M_PI / 180),         # maxVel
    1000000 * (M_PI / 180),     # maxAcc
    0,                          # blendT
    0                           # blendR
)

    print("🚨 Moving to singularity pose...")
    robot_interface.getMotionControl().moveLine(
    waypoint_2_p,
    250 * (M_PI / 180),
    1000 * (M_PI / 180),
    0,
    0
)


if __name__ == "__main__":
    # Connect and login to RPC
    rpc = pyaubo_sdk.RpcClient()
    rpc.connect(robot_ip, rpc_port)
    rpc.login("aubo", "123456")
    robot_name = rpc.getRobotNames()[0]
    robot_interface = rpc.getRobotInterface(robot_name)

    # Connect and login to RTDE
    rtde = pyaubo_sdk.RtdeClient()
    rtde.connect(robot_ip, rtde_port)
    rtde.login("aubo", "123456")

    # Subscribe to log messages from robot
    topic = rtde.setTopic(False, ["R1_message"], 200, 0)
    if topic < 0:
        print("❌ Failed to set topic.")
        sys.exit(1)

    rtde.subscribe(topic, subscribe_callback)

    # Move and watch for singularity errors
    movel_singularity(robot_interface)

    # Keep script alive to receive log messages
    while True:
        time.sleep(1)
