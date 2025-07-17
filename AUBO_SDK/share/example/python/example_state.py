#! /usr/bin/env python
# coding=utf-8

"""
Get robot arm state information

Steps:
Step 1: Connect to the RPC service
Step 2: Robot login
Step 3: Get robot arm state information
"""

import pyaubo_sdk

robot_ip = "192.168.0.141"  # Server IP address
robot_port = 30004  # Port number
M_PI = 3.14159265358979323846
robot_rpc_client = pyaubo_sdk.RpcClient()


# Get robot arm state information
def exampleState(robot_name):
    # Get robot mode state
    robot_mode_type = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getRobotModeType()
    print("Robot mode state:", robot_mode_type)
    # Get safety mode
    safety_mode_type = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getSafetyModeType()
    print("Safety mode:", safety_mode_type)
    # Is robot steady
    is_steady = robot_rpc_client.getRobotInterface(robot_name).getRobotState().isSteady()
    print("Is robot steady:", is_steady)
    # Is robot within safety limits
    is_within_safety_limits = robot_rpc_client.getRobotInterface(robot_name).getRobotState().isWithinSafetyLimits()
    print("Is robot within safety limits:", is_within_safety_limits)
    # Get TCP pose
    tcp_pose = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getTcpPose()
    print("TCP pose:", tcp_pose)
    # Get current target TCP pose
    target_tcp_pose = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getTargetTcpPose()
    print("Current target TCP pose:", target_tcp_pose)
    # Get tool pose (without TCP offset)
    tool_pose = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getToolPose()
    print("Tool pose (without TCP offset):", tool_pose)
    # Get TCP speed
    tcp_speed = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getTcpSpeed()
    print("TCP speed:", tcp_speed)
    # Get TCP force/torque
    tcp_force = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getTcpForce()
    print("TCP force/torque:", tcp_force)
    # Get elbow position
    elbow_postion = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getElbowPosistion()
    print("Elbow position:", elbow_postion)
    # Get elbow velocity
    elbow_velocity = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getElbowVelocity()
    print("Elbow velocity:", elbow_velocity)
    # Get base force/torque
    base_force = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getBaseForce()
    print("Base force/torque:", base_force)
    # Get TCP target pose
    tcp_target_pose = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getTcpTargetPose()
    print("TCP target pose:", tcp_target_pose)
    # Get TCP target speed
    tcp_target_speed = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getTcpTargetSpeed()
    print("TCP target speed:", tcp_target_speed)
    # Get TCP target force/torque
    tcp_target_force = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getTcpTargetForce()
    print("TCP target force/torque:", tcp_target_force)
    # Get joint state
    joint_state = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointState()
    print("Joint state:", joint_state)
    # Get joint servo mode
    joint_servo_mode = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointServoMode()
    print("Joint servo mode:", joint_servo_mode)
    # Get joint positions
    joint_positions = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointPositions()
    print("Joint positions:", joint_positions)
    # Get joint speeds
    joint_speeds = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointSpeeds()
    print("Joint speeds:", joint_speeds)
    # Get joint accelerations
    joint_acc = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointAccelerations()
    print("Joint accelerations:", joint_acc)
    # Get joint torque sensors
    joint_torque_sensors = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointTorqueSensors()
    print("Joint torque sensors:", joint_torque_sensors)
    # Get base force sensor readings
    base_force_sensors = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getBaseForceSensor()
    print("Base force sensor readings:", base_force_sensors)
    # Get TCP force sensor readings
    tcp_force_sensors = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getTcpForceSensors()
    print("TCP force sensor readings:", tcp_force_sensors)
    # Get joint currents
    joint_currents = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointCurrents()
    print("Joint currents:", joint_currents)
    # Get joint voltages
    joint_voltages = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointVoltages()
    print("Joint voltages:", joint_voltages)
    # Get joint temperatures
    joint_temperatures = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointTemperatures()
    print("Joint temperatures:", joint_temperatures)
    # Get joint UniqueId
    joint_unique_ids = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointUniqueIds()
    print("Joint UniqueId:", joint_unique_ids)
    # Get joint firmware versions
    joint_firmware_versions = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointFirmwareVersions()
    print("Joint firmware versions:", joint_firmware_versions)
    # Get joint hardware versions
    joint_hardward_versions = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointHardwareVersions()
    print("Joint hardware versions:", joint_hardward_versions)
    # Get master board UniqueId
    master_board_unique_id = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getMasterBoardUniqueId()
    print("Master board UniqueId:", master_board_unique_id)
    # Get MasterBoard firmware version
    master_board_firmware_version = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getMasterBoardFirmwareVersion()
    print("MasterBoard firmware version:", master_board_firmware_version)
    # Get MasterBoard hardware version
    master_board_hardware_version = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getMasterBoardHardwareVersion()
    print("MasterBoard hardware version:", master_board_hardware_version)
    # Get slave board UniqueId
    slave_board_unique_id = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getSlaveBoardUniqueId()
    print("Slave board UniqueId:", slave_board_unique_id)
    # Get SlaveBoard firmware version
    slave_board_firmware_version = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getSlaveBoardFirmwareVersion()
    print("SlaveBoard firmware version:", slave_board_firmware_version)
    # Get SlaveBoard hardware version
    slave_board_hardware_version = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getSlaveBoardHardwareVersion()
    print("SlaveBoard hardware version:", slave_board_hardware_version)
    # Get tool UniqueId
    tool_unique_id = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getToolUniqueId()
    print("Tool UniqueId:", tool_unique_id)
    # Get tool firmware version
    tool_firmware_version = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getToolFirmwareVersion()
    print("Tool firmware version:", tool_firmware_version)
    # Get tool hardware version
    tool_hardware_version = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getToolHardwareVersion()
    print("Tool hardware version:", tool_hardware_version)
    # Get pedestal UniqueId
    pedestal_unique_id = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getPedestalUniqueId()
    print("Pedestal UniqueId:", pedestal_unique_id)
    # Get pedestal firmware version
    pedestal_firmware_version = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getPedestalFirmwareVersion()
    print("Pedestal firmware version:", pedestal_firmware_version)
    # Get pedestal hardware version
    pedestal_hardware_version = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getPedestalHardwareVersion()
    print("Pedestal hardware version:", pedestal_hardware_version)
    # Get joint target positions
    joint_target_positions = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointTargetPositions()
    print("Joint target positions:", joint_target_positions)
    # Get joint target speeds
    joint_target_speeds = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointTargetSpeeds()
    print("Joint target speeds:", joint_target_speeds)
    # Get joint target accelerations
    joint_target_acc = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointTargetAccelerations()
    print("Joint target accelerations:", joint_target_acc)
    # Get joint target torques
    joint_target_torques = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointTargetTorques()
    print("Joint target torques:", joint_target_torques)
    # Get joint target currents
    joint_target_currents = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointTargetCurrents()
    print("Joint target currents:", joint_target_currents)
    # Get control box temperature
    control_box_temperature = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getControlBoxTemperature()
    print("Control box temperature:", control_box_temperature)
    # Get main voltage
    main_voltage = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getMainVoltage()
    print("Main voltage:", main_voltage)
    # Get main current
    main_current = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getMainCurrent()
    print("Main current:", main_current)
    # Get robot voltage
    robot_voltage = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getRobotVoltage()
    print("Robot voltage:", robot_voltage)
    # Get robot current
    robot_current = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getRobotCurrent()
    print("Robot current:", robot_current)


if __name__ == '__main__':
    robot_rpc_client.connect(robot_ip, robot_port)  # Connect to RPC service
    if robot_rpc_client.hasConnected():
        print("Robot rpc_client connected successfully!")
        robot_rpc_client.login("aubo", "123456")  # Robot login
        if robot_rpc_client.hasLogined():
            print("Robot rpc_client logged in successfully!")
            robot_name = robot_rpc_client.getRobotNames()[0]  # Get robot name
            exampleState(robot_name)  # Get robot arm state information
