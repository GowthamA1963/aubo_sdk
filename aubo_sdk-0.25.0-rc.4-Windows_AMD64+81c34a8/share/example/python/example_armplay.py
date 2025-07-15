# We'll fix the Python code based on the user's last input,
# addressing:
# 1. `pathBufferEval` returning -5
# 2. Improved safety and clarity in path buffering
# 3. Handle return values and timeouts more robustly


#! /usr/bin/env python
# coding=utf-8

import pyaubo_sdk
import time
import json
import sys
import os

robot_ip = "192.168.0.141"
robot_port = 30004
M_PI = 3.141592653589793

robot_rpc_client = pyaubo_sdk.RpcClient()

def waitArrival(impl):
    cnt = 0
    while impl.getMotionControl().getExecId() == -1:
        cnt += 1
        if cnt > 20:
            print("❌ Motion failed or did not start.")
            return -1
        time.sleep(0.05)
    exec_id = impl.getMotionControl().getExecId()
    while True:
        current_id = impl.getMotionControl().getExecId()
        if exec_id != current_id:
            break
        time.sleep(0.05)
    print("✅ Motion arrived at target.")

def waitMovePathBufferFinished(impl):
    while impl.getMotionControl().getExecId() == -1:
        time.sleep(0.05)
    while True:
        exec_id = impl.getMotionControl().getExecId()
        if exec_id == -1:
            break
        time.sleep(0.05)
    print("✅ Path buffer execution completed.")

if __name__ == '__main__':
    robot_rpc_client.setRequestTimeout(10000)
    robot_rpc_client.connect(robot_ip, robot_port)

    if not robot_rpc_client.hasConnected():
        print("❌ Failed to connect to robot.")
        sys.exit(1)

    print("✅ Robot RPC client connected successfully!")
    robot_rpc_client.login("aubo", "123456")

    if not robot_rpc_client.hasLogined():
        print("❌ Login failed.")
        sys.exit(1)

    print("✅ Robot RPC client logged in successfully!")

    # Use raw string for Windows path
    json_file_path = r'D:\aubo_sdk-0.25.0-rc.4-Windows_AMD64+81c34a8\aubo_sdk-0.25.0-rc.4-Windows_AMD64+81c34a8\share\example\c++\trajs\aubo-joint-test-1014.armplay'

    if not os.path.exists(json_file_path):
        print(f"❌ File not found: {json_file_path}")
        sys.exit(1)

    with open(json_file_path, 'r') as f:
        input_data = json.load(f)

    traj = input_data['jointlist']
    interval = input_data.get('interval', 0.05)  # safer default
    print("ℹ️ Sampling interval:", interval)

    traj_sz = len(traj)
    if traj_sz == 0:
        print("⚠️ No waypoints found in the trajectory.")
        sys.exit(1)

    print(f"ℹ️ Loaded {traj_sz} waypoints.")
    robot_name = robot_rpc_client.getRobotNames()[0]
    mc = robot_rpc_client.getRobotInterface(robot_name).getMotionControl()

    q1 = traj[0]
    print("➡️ Moving to first waypoint:", q1)
    mc.moveJoint(q1, M_PI, M_PI, 0.0, 0.0)
    waitArrival(robot_rpc_client.getRobotInterface(robot_name))

    print("🧹 Releasing old path buffer (if any)...")
    mc.pathBufferFree("rec")
    print("📦 Allocating new path buffer: rec")
    mc.pathBufferAlloc("rec", 2, traj_sz)

    offset = 0
    while offset < traj_sz:
        batch = traj[offset:offset + 10]
        print(f"➕ Appending points {offset} to {offset + len(batch)} to path buffer")
        mc.pathBufferAppend("rec", batch)
        offset += 10

    print("🧠 Evaluating path buffer...")
    eval_result = mc.pathBufferEval("rec", [], [], interval)
    print("ℹ️ pathBufferEval result:", eval_result)

    if eval_result != 0:
        print("❌ Path buffer evaluation failed. Exiting.")
        sys.exit(1)

    print("⏳ Waiting for buffer to become valid...")
    wait_counter = 0
    while not mc.pathBufferValid("rec"):
        time.sleep(0.1)
        wait_counter += 1
        if wait_counter > 100:
            print("❌ Timeout: Path buffer did not become valid.")
            sys.exit(1)

    print("🚀 Executing buffered motion...")
    mc.movePathBuffer("rec")
    waitMovePathBufferFinished(robot_rpc_client.getRobotInterface(robot_name))

    robot_rpc_client.logout()
    robot_rpc_client.disconnect()
    print("🔌 Disconnected from robot.")


