#! /usr/bin/env python
# coding=utf-8

"""
trackJoint motion

Steps:
1. Connect to the RPC service, log in to the robot, set the RPC request timeout
2. Read the .offt trajectory file
3. Move joints to the first point in the trajectory
4. Perform trackJoint motion
5. Stop trackJoint motion
6. Disconnect the RPC connection
"""
import pyaubo_sdk
import time

robot_ip = "192.168.0.141"  # Server IP address
robot_port = 30004       # Port number
M_PI = 3.14159265358979323846
robot_rpc_client = pyaubo_sdk.RpcClient()

# Blocking wait for arrival
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

def trackJ():
    robot_name = robot_rpc_client.getRobotNames()[0]  # Get robot name
    robot = robot_rpc_client.getRobotInterface(robot_name)

    # Read trajectory file and load trajectory points
    file = open(r'D:\AUBO_SDK\AUBO_SDK\share\example\c++\trajs\record6.offt')
    traj = []
    for line in file:
        str_list = line.split(",")
        float_list = []
        for strs in str_list:
            float_list.append(float(strs))
        traj.append(float_list)

    traj_sz = len(traj)
    if traj_sz == 0:
        print("No trajectory points loaded")
    else:
        print("Number of loaded trajectory points: ", traj_sz)

    # Move joints to the first point
    # The current position should match the first point in the trajectory to avoid overshoot
    print("Moving to the first trajectory point")
    mc = robot.getMotionControl()
    mc.setSpeedFraction(0.8)
    mc.moveJoint(traj[0], M_PI, M_PI, 0., 0.)
    wait_arrival(robot)

    # Perform trackJoint motion
    traj.remove(traj[0])
    for q in traj:
        traj_queue_size = mc.getTrajectoryQueueSize()
        print("Trajectory queue size: ", traj_queue_size)
        while traj_queue_size > 8:
            traj_queue_size = mc.getTrajectoryQueueSize()
            time.sleep(0.001)
        mc.trackJoint(q, 0.02, 0.5, 1)

    # Stop trackJoint motion
    mc.stopJoint(1)

    # Wait for motion to finish
    is_steady = robot.getRobotState().isSteady()
    while is_steady is False:
        is_steady = robot.getRobotState().isSteady()
        time.sleep(0.005)
    
    print("trackJoint motion finished")
    return 0


if __name__ == '__main__':
    robot_rpc_client.setRequestTimeout(1000)  # Set RPC request timeout
    robot_rpc_client.connect(robot_ip, robot_port)  # Connect to RPC service
    if robot_rpc_client.hasConnected():
        print("Robot RPC client connected successfully!")
        robot_rpc_client.login("aubo", "123456")  # Robot login
        if robot_rpc_client.hasLogined():
            print("Robot RPC client logged in successfully!")
            trackJ()
            robot_rpc_client.disconnect()  # Disconnect RPC connection

