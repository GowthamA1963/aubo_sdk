#! /usr/bin/env python
# coding=utf-8

import numpy as np
from scipy.spatial.transform import Rotation as R

# Convert Euler angles to quaternion
def exampleRpyToQuat():
    print("🔁 Convert Euler angles to quaternion")
    rpy = [0.611, 0.785, 0.960]  # roll, pitch, yaw in radians
    quat = R.from_euler('xyz', rpy).as_quat()  # [x, y, z, w]
    print("Quaternion [x, y, z, w]:", quat)
    return quat

# Convert quaternion to Euler angles
def exampleQuatToRpy(quat):
    print("🔁 Convert quaternion to Euler angles")
    r = R.from_quat(quat)
    rpy = r.as_euler('xyz')
    print("Euler angles (rpy):", rpy)
    return rpy

# Convert pose to transformation matrix
def pose_to_matrix(pose):
    trans = np.array(pose[:3])
    r = R.from_euler('xyz', pose[3:])
    rotm = r.as_matrix()
    mat = np.eye(4)
    mat[:3, :3] = rotm
    mat[:3, 3] = trans
    return mat

# Convert transformation matrix to pose
def matrix_to_pose(mat):
    trans = mat[:3, 3]
    r = R.from_matrix(mat[:3, :3])
    rpy = r.as_euler('xyz')
    return list(trans) + list(rpy)

# Simulate poseTrans (TCP = flange ⊕ offset)
def pose_trans(base_pose, offset_pose):
    T_base = pose_to_matrix(base_pose)
    T_offset = pose_to_matrix(offset_pose)
    T_tcp = np.dot(T_base, T_offset)
    return matrix_to_pose(T_tcp)

# Simulate poseInverse
def pose_inverse(pose):
    T = pose_to_matrix(pose)
    T_inv = np.linalg.inv(T)
    return matrix_to_pose(T_inv)

# Calculate TCP pose from flange pose and TCP offset
def example_flange_to_tcp():
    print("📍 flange → tcp")
    flange_pose = [0.5, 0.0, 0.3, 0.0, 0.0, 0.0]  # example
    tcp_offset = [0.01, 0.02, 0.03, 0.1, 0.2, 0.0]
    tcp_pose = pose_trans(flange_pose, tcp_offset)
    print("TCP pose in base:", tcp_pose)
    return tcp_pose

# Calculate flange pose from TCP pose and TCP offset
def example_tcp_to_flange():
    print("📍 tcp → flange")
    tcp_pose = [0.51, 0.02, 0.33, 0.1, 0.2, 0.0]  # example
    tcp_offset = [0.01, 0.02, 0.03, 0.1, 0.2, 0.0]
    tcp_offset_inv = pose_inverse(tcp_offset)
    flange_pose = pose_trans(tcp_pose, tcp_offset_inv)
    print("Flange pose in base:", flange_pose)
    return flange_pose

if __name__ == '__main__':
    quat = exampleRpyToQuat()
    exampleQuatToRpy(quat)
    example_flange_to_tcp()
    example_tcp_to_flange()
