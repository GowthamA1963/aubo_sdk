#! /usr/bin/env python
# coding=utf-8

import time
import math
import pyaubo_sdk

robot_ip = "192.168.0.141"
robot_port = 30004
M_PI = 3.14159265358979323846
robot_rpc_client = pyaubo_sdk.RpcClient()

waypoint1 = []
waypoint2 = []
waypoint3 = []

def get_circle_waypoint():
    global waypoint1, waypoint2, waypoint3

    z1 = 0.26319
    y1 = 0.7
    x1 = math.sqrt(pow(0.2, 2) - pow(y1 - 0.54855, 2) - pow(z1 - 0.26319, 2))
    waypoint1 = [x1, y1, z1, 3.14, 0.00, 3.14]

    z2 = 0.26319
    y2 = 0.55
    x2 = math.sqrt(pow(0.2, 2) - pow(y2 - 0.54855, 2) - pow(z2 - 0.26319, 2))
    waypoint2 = [x2, y2, z2, 3.14, 0.00, 3.14]

    z3 = 0.26319
    y3 = 0.35
    x3 = math.sqrt(pow(0.2, 2) - pow(y3 - 0.54855, 2) - pow(z3 - 0.26319, 2))
    waypoint3 = [x3, y3, z3, 3.14, 0.00, 3.14]

def example_movec(robot_name):
    get_circle_waypoint()
    iface = robot_rpc_client.getRobotInterface(robot_name).getMotionControl()

    iface.moveLine(waypoint1, math.radians(180), math.radians(1000000), 0, 0)
    time.sleep(1)

    ret = iface.moveCircle(waypoint2, waypoint3, math.radians(180), math.radians(1000000), 0, 0)

    if ret == 0:
        print("✅ Arc motion succeeded!")
    else:
        print(f"❌ Arc motion failed! Error code: {ret}")

if __name__ == '__main__':
    robot_rpc_client.connect(robot_ip, robot_port)
    if robot_rpc_client.hasConnected():
        print("✅ Connected to robot")
        robot_rpc_client.login("aubo", "123456")
        if robot_rpc_client.hasLogined():
            print("✅ Logged in successfully!")
            robot_name = robot_rpc_client.getRobotNames()[0]

            try:
                while True:
                    example_movec(robot_name)
                    time.sleep(0.5)  # optional delay between loops
            except KeyboardInterrupt:
                print("🛑 Stopped by user (Ctrl+C)")
