#! /usr/bin/env python
# coding=utf-8

"""
servoCartesian Motion Example

Steps:
1. Connect to the RPC service, log in to the robot, set RPC request timeout
2. Read the .txt trajectory file
3. Move joints to the first point in the trajectory
4. Enable servo mode
5. Perform servoCartesian motion
6. Disable servo mode
7. Disconnect RPC connection
"""
import pyaubo_sdk
import time

robot_ip = "192.168.0.141"  # Server IP address
robot_port = 30004      # Port number
M_PI = 3.14159265358979323846
robot_rpc_client = pyaubo_sdk.RpcClient()


# Blocking wait for motion to finish
def wait_arrival(robot_interface):
    max_retry_count = 5
    cnt = 0

    # Get current motion command ID
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


def servo_cartesian():
    robot_name = robot_rpc_client.getRobotNames()[0]  # Get robot name
    robot_interface = robot_rpc_client.getRobotInterface(robot_name)

    # Read trajectory file and load trajectory points
    # Note: cartesian-heart-L.txt is a Cartesian trajectory file for S3 series,
    # and the orientation unit in the file is degrees
    file = open(r'D:\AUBO_SDK\AUBO_SDK\share\example\c++\trajs\cartesian-heart-L.txt')
    traj = []
    for line in file:
        str_list = line.split(",")
        float_list = []
        for strs in str_list:
            float_list.append(float(strs))
        # Convert orientation from degrees to radians
        for i in range(3, 6):
            float_list[i] = float_list[i] / 180 * M_PI
        traj.append(float_list)

    traj_sz = len(traj)
    if traj_sz == 0:
        print("No trajectory points loaded")
        return 0
    else:
        print("Number of loaded trajectory points: ", traj_sz)

    robot_name = robot_rpc_client.getRobotNames()[0]  # Get robot name

    # Get current joint positions (unit: rad)
    current_q = robot_rpc_client.getRobotInterface(robot_name).getRobotState().getJointPositions()
    # Inverse kinematics for the first trajectory point
    res = robot_rpc_client.getRobotInterface(robot_name).getRobotAlgorithm().inverseKinematics(current_q, traj[0])
    if res[1] != 0:
        print("Inverse kinematics failed for the first waypoint, return value:", res[1])
        return -1

    # Move joints to the first point in the trajectory
    # The current position should match the first point to avoid overshoot
    mc = robot_interface.getMotionControl()
    mc.moveJoint(res[0], 80/180*M_PI, 60/180*M_PI, 0., 0.)
    ret = wait_arrival(robot_interface)
    if ret == 0:
        print("Moved to waypoint 1 successfully")
    else:
        print("Failed to move to waypoint 1")
        return -1

    # Enable servo mode
    robot_interface.getMotionControl().setServoMode(True)
    i = 0
    while not mc.isServoModeEnabled():
        i = i + 1
        if i > 5:
            print("Failed to enable Servo mode! Current Servo mode:", mc.isServoModeEnabled())
            return -1
        time.sleep(0.005)

    traj.remove(traj[0])
    for p in traj:
        # Cartesian servo motion
        mc.servoCartesian(p, 0.0, 0.0, 0.1, 0.0, 0.0)
        time.sleep(0.05)

    # Disable servo mode
    mc.setServoMode(False)
    i = 0
    while mc.isServoModeEnabled():
        i = i + 1
        if i > 5:
            print("Failed to disable Servo mode! Current Servo mode:", mc.isServoModeEnabled())
            return -1
        time.sleep(0.005)
    print("servoCartesian motion finished")
    return 0


if __name__ == '__main__':
    robot_rpc_client.setRequestTimeout(1000)  # Set RPC request timeout
    robot_rpc_client.connect(robot_ip, robot_port)  # Connect to RPC service
    if robot_rpc_client.hasConnected():
        print("RPC connection successful!")
        robot_rpc_client.login("aubo", "123456")  # Robot login
        servo_cartesian()  # Cartesian servo motion example
        robot_rpc_client.disconnect()  # Disconnect RPC
    else:
        print("RPC connection failed!")
