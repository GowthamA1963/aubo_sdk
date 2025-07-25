#! /usr/bin/env python
# coding=utf-8

"""
PathBuffer Motion
Note: The trajectory in the offline trajectory file is relative to the user coordinate system.

Steps:
Step 1: Connect to the RPC service, log in to the robot, set the RPC request timeout
Step 2: Read the .csv trajectory file and load trajectory points
Step 3: Convert the poses in the trajectory file to poses relative to the base coordinate system,
    solve for joint angles via inverse kinematics,
    add them to the "rec" buffer
Step 4: Move joints to the first point,
    execute the buffered path
"""
import pyaubo_sdk
import time

robot_ip = "192.168.0.141"  # Server IP address
robot_port = 30004      # Port number
M_PI = 3.14159265358979323846
robot_rpc_client = pyaubo_sdk.RpcClient()


# Blocking wait
def waitArrival(impl):
    cnt = 0
    while impl.getMotionControl().getExecId() == -1:
        cnt += 1
        if cnt > 5:
            print("Motion fail!")
            return -1
        time.sleep(0.05)
    print("getExecId: ", impl.getMotionControl().getExecId())
    id = impl.getMotionControl().getExecId()
    while True:
        id1 = impl.getMotionControl().getExecId()
        if id != id1:
            break
        time.sleep(0.05)


# Wait for MovePathBuffer to finish
def waitMovePathBufferFinished(impl):
    while impl.getMotionControl().getExecId() == -1:
        time.sleep(0.05)
    while True:
        ids = impl.getMotionControl().getExecId()
        if ids == -1:
            break
        time.sleep(0.05)


if __name__ == '__main__':
    robot_rpc_client.setRequestTimeout(1000)  # Set RPC request timeout
    robot_rpc_client.connect(robot_ip, robot_port)  # Connect to RPC service
    if robot_rpc_client.hasConnected():
        print("Robot rcp_client connected successfully!")
        robot_rpc_client.login("aubo", "123456")  # Robot login
        if robot_rpc_client.hasLogined():
            print("Robot rcp_client logined successfully!")

            robot_name = robot_rpc_client.getRobotNames()[0]  # Get robot name
            robot = robot_rpc_client.getRobotInterface(robot_name)

            # Read trajectory file and load trajectory points
            file = open(r'D:\AUBO_SDK\AUBO_SDK\share\example\c++\trajs\CoffeCappuccino-heart-R_filtered.csv')
            traj = []
            for line in file:
                str_list = line.split(",")
                float_list = []
                for strs in str_list:
                    float_list.append(float(strs))
                traj.append(float_list)

            traj_sz = len(traj)
            if traj_sz == 0:
                print("No trajectory points")
            else:
                print("Number of loaded trajectory points: ", traj_sz)

            tcp_offset = [-0.093, 0.0007249, 0.152, 90.66 / 180.0 * M_PI, -0.7635 / 180.0 * M_PI, -91.49 / 180.0 * M_PI]

            coord_q0 = [-1.627214, -0.360182, 1.783065, -1.063912, -1.642473, -1.510366]
            coord_q1 = [-0.806772, -0.344142, 1.806783, -1.079834, -0.824188, -1.444983]
            coord_q2 = [-0.702519, -0.105247, 2.113576, -1.022056, -0.720357, -1.430912]

            robot.getRobotConfig().setTcpOffset(tcp_offset)  # Set TCP offset
            time.sleep(1)

            coord_p0 = robot.getRobotAlgorithm().forwardKinematics(coord_q0)[0]
            coord_p1 = robot.getRobotAlgorithm().forwardKinematics(coord_q1)[0]
            coord_p2 = robot.getRobotAlgorithm().forwardKinematics(coord_q2)[0]

            coord_p = [coord_p0, coord_p1, coord_p2]
            # Calculate the pose of the user coordinate system relative to the base coordinate system
            coord = robot_rpc_client.getMath().calibrateCoordinate(coord_p, 0)[0]

            print("TCP offset: ", tcp_offset)
            print("User coordinate system: ", coord)

            current_q = robot.getRobotState().getJointPositions()
            traj_q = []
            for p in traj:
                # Given the trajectory relative to the user coordinate system and the pose of the user coordinate system relative to the base coordinate system,
                # calculate the trajectory pose relative to the base coordinate system
                rp = robot_rpc_client.getMath().poseTrans(coord, p)
                # Inverse kinematics to get joint angles
                q = robot.getRobotAlgorithm().inverseKinematics(current_q, rp)[0]
                current_q = q
                traj_q.append(q)
                print("q: ", q)

            # Move joints to the first point
            print("goto p1")
            mc = robot.getMotionControl()
            mc.moveJoint(traj_q[0], M_PI, M_PI, 0., 0.)
            waitArrival(robot)

            print("pathBufferAlloc")
            # mc.pathBufferFree("rec")  # Release path buffer
            mc.pathBufferAlloc("rec", 3, traj_sz)  # Create a new path point buffer

            # Add waypoints from traj_q to the "rec" buffer
            # Add every 10 waypoints as a list
            # If the remaining waypoints are less than or equal to 10, add them as the last group
            offset = 10
            it = 0
            while True:
                print("pathBufferAppend ", offset)
                mc.pathBufferAppend("rec", traj_q[it:it + 10:1])  # Add waypoints to path buffer
                it += 10
                if offset + 10 >= traj_sz:
                    print("pathBufferAppend ", traj_sz)
                    mc.pathBufferAppend("rec", traj_q[it:traj_sz:1])
                    break
                offset += 10

            interval = 0
            print("pathBufferEval ", mc.pathBufferEval("rec", [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1],
                                   interval))  # Compute/optimize, will not recalculate if parameters are the same
            while not mc.pathBufferValid("rec"):
                print("pathBufferValid: ", mc.pathBufferValid("rec"))  # Check if buffer is valid
                time.sleep(0.005)
            mc.movePathBuffer("rec")  # Execute buffered path
            waitMovePathBufferFinished(robot_rpc_client.getRobotInterface(robot_name))
            print("end movePathBuffer")
            robot_rpc_client.disconnect()  # Disconnect RPC connection

