import threading
import pyaubo_sdk
import time
import csv
from datetime import datetime
from example_movej import example_movej

robot_ip = "192.168.0.182"
rtde_port = 30010
rpc_port = 30004

robot_rtde_client = pyaubo_sdk.RtdeClient()
mutex = threading.Lock()
stop_event = threading.Event()  # ✅ shared event

# Shared state for Callback 2
latest_joint_temperatures = [0] * 6
latest_joint_modes = [''] * 6
latest_main_voltage = 0.0
latest_robot_voltage = 0.0

# Setup CSV logger
csv_file = open("rtde_full_log.csv", mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow([
    "Timestamp",
    "Joint1", "Joint2", "Joint3", "Joint4", "Joint5", "Joint6",
    "Current1", "Current2", "Current3", "Current4", "Current5", "Current6",
    "TCP_X", "TCP_Y", "TCP_Z", "TCP_RX", "TCP_RY", "TCP_RZ",
    "RobotMode", "SafetyMode", "RuntimeState", "LineNum",
    "Temp1", "Temp2", "Temp3", "Temp4", "Temp5", "Temp6",
    "JointMode1", "JointMode2", "JointMode3", "JointMode4", "JointMode5", "JointMode6",
    "MainVoltage", "RobotVoltage"
])

# ========== Callback 1 ==========
def subscribe_callback1(parser):
    global latest_joint_temperatures, latest_joint_modes, latest_main_voltage, latest_robot_voltage

    with mutex:
        print("[Callback 1 Triggered]")
        actual_q_ = parser.popVectorDouble()
        print('@actual_q_: {}'.format(actual_q_))
        actual_current_ = parser.popVectorDouble()
        print('@actual_current_: {}'.format(actual_current_))
        robot_mode_ = parser.popRobotModeType()
        print('@robot_mode_: {}'.format(robot_mode_))
        safety_mode_ = parser.popSafetyModeType()
        print('@safety_mode_: {}'.format(safety_mode_))
        runtime_state_ = parser.popRuntimeState()
        print('@runtime_state_: {}'.format(runtime_state_))
        line_ = parser.popInt32()
        print('@line_: {}'.format(line_))
        actual_TCP_pose_ = parser.popVectorDouble()
        print('@actual_TCP_pose_: {}'.format(actual_TCP_pose_))


        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        csv_writer.writerow([
            now,
            *actual_q_,
            *actual_current_,
            *actual_TCP_pose_,
            str(robot_mode_),
            str(safety_mode_),
            str(runtime_state_),
            line_,
            *latest_joint_temperatures,
            *[str(m) for m in latest_joint_modes],
            latest_main_voltage,
            latest_robot_voltage
        ])
        csv_file.flush()

# ========== Callback 2 ==========
def subscribe_callback2(parser):
    global latest_joint_temperatures, latest_joint_modes, latest_main_voltage, latest_robot_voltage

    with mutex:
        print("[Callback 2 Triggered]")
        joint_temperatures_ = parser.popVectorDouble()
        print('@joint_temperatures_: {}'.format(joint_temperatures_))
        joint_mode_ = parser.popVectorJointStateType()
        print('@joint_mode_: {}'.format(joint_mode_))
        actual_main_voltage_ = parser.popDouble()
        print('@actual_main_voltage_: {}'.format(actual_main_voltage_))
        actual_robot_voltage_ = parser.popDouble()
        print('@actual_robot_voltage_: {}'.format(actual_robot_voltage_))

        # ✅ Store in shared variables for use in Callback 1
        latest_joint_temperatures = joint_temperatures_
        latest_joint_modes = joint_mode_
        latest_main_voltage = actual_main_voltage_
        latest_robot_voltage = actual_robot_voltage_


# ========== RTDE Monitoring ==========
def rtde_monitoring():
    topic1 = robot_rtde_client.setTopic(False, [
        "R1_actual_q", "R1_actual_current", "R1_robot_mode",
        "R1_safety_mode", "runtime_state", "line_number", "R1_actual_TCP_pose"
    ], 50, 0)

    topic2 = robot_rtde_client.setTopic(False, [
        "R1_joint_temperatures", "R1_joint_mode",
        "R1_actual_main_voltage", "R1_actual_robot_voltage"
    ], 10, 1)

    if topic1 != -1:
        robot_rtde_client.subscribe(topic1, subscribe_callback1)
        print("Subscribed to topic 1")
    else:
        print("Failed to subscribe to topic 1")

    if topic2 != -1:
        robot_rtde_client.subscribe(topic2, subscribe_callback2)
        print("Subscribed to topic 2")
    else:
        print("Failed to subscribe to topic 2")

    # Keep running until MoveJ completes
    while not stop_event.is_set():
        time.sleep(0.1)

    # Clean up subscriptions
    print("RTDE stopping...")
    robot_rtde_client.removeTopic(False, topic1)
    robot_rtde_client.removeTopic(False, topic2)

# ========== MoveJ Control ==========
def execute_motion():
    rpc_client = pyaubo_sdk.RpcClient()
    rpc_client.setRequestTimeout(1000)
    rpc_client.connect(robot_ip, rpc_port)
    if rpc_client.hasConnected():
        rpc_client.login("aubo", "123456")
        if rpc_client.hasLogined():
            print("[Motion] Logged in. Executing MoveJ")
            example_movej(rpc_client)
            rpc_client.logout()
            rpc_client.disconnect()
            print("[Motion] MoveJ completed.")
            stop_event.set()  # ✅ Signal RTDE thread to stop
        else:
            print("RPC login failed")
    else:
        print("RPC connection failed")

# ========== Main ==========
if __name__ == '__main__':
    robot_rtde_client.connect(robot_ip, rtde_port)
    if robot_rtde_client.hasConnected():
        robot_rtde_client.login("aubo", "123456")
        if robot_rtde_client.hasLogined():
            print("RTDE connected and logged in")

            t1 = threading.Thread(target=rtde_monitoring)
            t2 = threading.Thread(target=execute_motion)

            t1.start()
            t2.start()

            t1.join()
            t2.join()
        else:
            print("RTDE login failed")
    else:
        print("RTDE connection failed")

    csv_file.close()
    print("CSV logging complete. All threads exited cleanly.")
