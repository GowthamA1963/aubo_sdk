#! /usr/bin/env python
# coding=utf-8

import pyaubo_sdk
import sys

robot_ip = "192.168.0.141"
robot_port = 30004
robot_rpc_client = pyaubo_sdk.RpcClient()

def exampleConfig(robot_name):
    config = robot_rpc_client.getRobotInterface(robot_name).getRobotConfig()

    print("Robot name:", config.getName())
    print("Degrees of freedom:", config.getDof())
    print("Servo control cycle time:", config.getCycletime())
    print("Default tool acceleration:", config.getDefaultToolAcc())
    print("Default tool speed:", config.getDefaultToolSpeed())
    print("Default joint acceleration:", config.getDefaultJointAcc())
    print("Default joint speed:", config.getDefaultJointSpeed())
    print("Robot type code:", config.getRobotType())
    print("Robot sub-type code:", config.getRobotSubType())
    print("Control box type code:", config.getControlBoxType())
    print("Mounting pose:", config.getMountingPose())

    # Safe collision level
    try:
        level = 3  # Aubo typically supports 0 to 3
        config.setCollisionLevel(level)
        print("✅ Collision sensitivity level set to:", level)
    except Exception as e:
        print("⚠️ Failed to set collision level:", e)

    try:
        print("Collision sensitivity level:", config.getCollisionLevel())
    except Exception as e:
        print("⚠️ Failed to get collision level:", e)

    try:
        config.setCollisionStopType(1)
        print("✅ Collision stop type set to 1")
    except Exception as e:
        print("⚠️ Failed to set collision stop type:", e)

    try:
        print("Collision stop type:", config.getCollisionStopType())
    except Exception as e:
        print("⚠️ Failed to get collision stop type:", e)

    try:
        print("Robot DH parameters:", config.getKinematicsParam(True))
        print("DH compensation at 20°C:", config.getKinematicsCompensate(20))
    except Exception as e:
        print("⚠️ Kinematics info fetch failed:", e)

    try:
        print("Available TCP force sensor names:", config.getTcpForceSensorNames())
        print("TCP force offset:", config.getTcpForceOffset())
        print("Available base force sensor names:", config.getBaseForceSensorNames())
        print("Base force offset:", config.getBaseForceOffset())
    except Exception as e:
        print("⚠️ Force sensor info fetch failed:", e)

    print("Safety checksum CRC32:", config.getSafetyParametersCheckSum())
    print("Joint max positions:", config.getJointMaxPositions())
    print("Joint min positions:", config.getJointMinPositions())
    print("Joint max speeds:", config.getJointMaxSpeeds())
    print("Joint max accelerations:", config.getJointMaxAccelerations())
    print("TCP max speeds:", config.getTcpMaxSpeeds())
    print("TCP max accelerations:", config.getTcpMaxAccelerations())
    print("Robot installation posture:", config.getGravity())
    print("TCP offset:", config.getTcpOffset())

    payload = config.getPayload()
    print("End effector payload:")
    print("  mass:", payload[0])
    print("  cog:", payload[1])
    print("  aom:", payload[2])
    print("  inertia:", payload[3])

    print("Firmware update process:", config.getFirmwareUpdateProcess())

if __name__ == '__main__':
    robot_rpc_client.connect(robot_ip, robot_port)
    if not robot_rpc_client.hasConnected():
        print("❌ Failed to connect to robot.")
        sys.exit(1)

    print("Robot rpc_client connected successfully!")
    robot_rpc_client.login("aubo", "123456")
    if not robot_rpc_client.hasLogined():
        print("❌ Login failed.")
        sys.exit(1)

    print("Robot rpc_client logged in successfully!")

    robot_name = robot_rpc_client.getRobotNames()[0]
    print("Connected robot:", robot_name)

    try:
        exampleConfig(robot_name)
    except Exception as e:
        print("❌ Error during configuration:", e)

    robot_rpc_client.logout()
    robot_rpc_client.disconnect()
    print("🔌 Disconnected from robot.")
