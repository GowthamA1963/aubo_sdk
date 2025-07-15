import threading
import pyaubo_sdk
import example_movej

robot_ip = "192.168.0.141"  # Replace with actual robot IP
robot_port = 30010
M_PI = 3.14159265358979323846

robot_rtde_client = pyaubo_sdk.RtdeClient()
mutex = threading.Lock()

# ========== Callback 1 ==========
def subscribe_callback1(parser):
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

# ========== Callback 2 ==========
def subscribe_callback2(parser):
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

# ========== Subscription Logic ==========
def example_subscribe():
    # Topic 1 - high frequency
    names_list1 = [
        "R1_actual_q", "R1_actual_current", "R1_robot_mode",
        "R1_safety_mode", "runtime_state", "line_number", "R1_actual_TCP_pose"
    ]
    topic1 = robot_rtde_client.setTopic(False, names_list1, 50, 0)
    if topic1 != -1:
        print("Subscribed to topic 1")
        robot_rtde_client.subscribe(topic1, subscribe_callback1)
    else:
        print("Failed to subscribe to topic 1")

    # Topic 2 - low frequency
    names_list2 = [
        "R1_joint_temperatures", "R1_joint_mode",
        "R1_actual_main_voltage", "R1_actual_robot_voltage"
    ]
    topic2 = robot_rtde_client.setTopic(False, names_list2, 10, 1)  # Increased freq to 10Hz for visibility
    if topic2 != -1:
        print("Subscribed to topic 2")
        robot_rtde_client.subscribe(topic2, subscribe_callback2)
    else:
        print("Failed to subscribe to topic 2")

    try:
        while True:
            cmd = input("Type 'stop' to end: ").strip().lower()
            if cmd == 'stop':
                print("Unsubscribing...")
                robot_rtde_client.removeTopic(False, topic1)
                robot_rtde_client.removeTopic(False, topic2)
                break
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")

# ========== Main ==========
if __name__ == '__main__':
    robot_rtde_client.connect(robot_ip, robot_port)
    if robot_rtde_client.hasConnected():
        print("Robot rtde_client connected successfully!")
        robot_rtde_client.login("aubo", "123456")
        if robot_rtde_client.hasLogined():
            print("Robot rtde_client logined successfully!")
            example_subscribe()
        else:
            print("Login failed!")
    else:
        print("Connection failed!")
