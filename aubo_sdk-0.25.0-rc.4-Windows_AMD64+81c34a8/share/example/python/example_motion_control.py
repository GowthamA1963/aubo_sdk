import threading
import time
import math
from pyaubo_sdk import RpcClient, RuntimeState

# Robot IP address
LOCAL_IP = "192.168.0.141"


def wait_for_queue_space(motion_function):
    """
    Wait for motion queue to have space. Calls the specified motion function until the return value is not 2 (2 means queue is full).
    :param motion_function: The motion function to execute
    """
    while motion_function() == 2:  # 2 means queue is full
        time.sleep(0.05)
    motion_function()


def execute_motion_sequence(motions):
    """
    Send motion commands until the stop event is set.
    :param motions: List of motion command functions
    """
    for motion in motions:
        if stop_event.is_set():
            return  # Stop sending motion commands if stop event is set
        wait_for_queue_space(motion)


def robot_motion_control(cli):
    """
    Control the robot to execute motions
    :param cli: RpcClient instance for communication with the robot
    """
    # Waypoints in joint angles (radians)
    joint_angle1 = [
        0.0 * (math.pi / 180), -15.0 * (math.pi / 180), 100.0 * (math.pi / 180),
        25.0 * (math.pi / 180), 90.0 * (math.pi / 180), 0.0 * (math.pi / 180)
    ]

    joint_angle2 = [
        35.92 * (math.pi / 180), -11.28 * (math.pi / 180), 59.96 * (math.pi / 180),
        -18.76 * (math.pi / 180), 90.0 * (math.pi / 180), 35.92 * (math.pi / 180)
    ]

    joint_angle3 = [
        41.04 * (math.pi / 180), -7.65 * (math.pi / 180), 98.80 * (math.pi / 180),
        16.44 * (math.pi / 180), 90.0 * (math.pi / 180), 11.64 * (math.pi / 180)
    ]

    joint_angle4 = [
        41.04 * (math.pi / 180), -27.03 * (math.pi / 180), 115.35 * (math.pi / 180),
        52.37 * (math.pi / 180), 90.0 * (math.pi / 180), 11.64 * (math.pi / 180)
    ]

    # Get robot name
    robot_name = rpc_cli.getRobotNames()[0]
    robot_interface = rpc_cli.getRobotInterface(robot_name)

    # Start runtime machine
    rpc_cli.getRuntimeMachine().start()

    time.sleep(1)

    # Set motion speed fraction
    robot_interface.getMotionControl().setSpeedFraction(1)

    # List of motion functions
    motions = [
        lambda: robot_interface.getMotionControl().moveJoint(joint_angle1, 80 * (math.pi / 180),
                                                             60 * (math.pi / 180), 0.0, 0),
        lambda: robot_interface.getMotionControl().moveJoint(joint_angle2, 80 * (math.pi / 180),
                                                             60 * (math.pi / 180), 0.0, 0),
        lambda: robot_interface.getMotionControl().moveJoint(joint_angle3, 80 * (math.pi / 180),
                                                             60 * (math.pi / 180), 0.0, 0),
        lambda: robot_interface.getMotionControl().moveJoint(joint_angle4, 80 * (math.pi / 180),
                                                             60 * (math.pi / 180), 0.0, 0)
    ]

    # Loop to execute motion commands until runtime machine is stopped or stop event is set
    while rpc_cli.getRuntimeMachine().getStatus() != RuntimeState.Stopped and not stop_event.is_set():
        execute_motion_sequence(motions)


def control_operations(cli):
    while not stop_event.is_set():
        input_cmd = input("Enter command (p/r/s): p for pause, r for resume, s for stop\n")

        if input_cmd == "p":
            # Pause runtime machine
            cli.getRuntimeMachine().pause()
            print("Motion paused")
        elif input_cmd == "r":
            # Resume runtime machine
            cli.getRuntimeMachine().resume()
            print("Motion resumed")
        elif input_cmd == "s":
            # Abort runtime machine
            cli.getRuntimeMachine().abort()
            robot_name = cli.getRobotNames()[0]
            robot_interface = cli.getRobotInterface(robot_name)
            # Stop motion
            robot_interface.getMotionControl().stopJoint(30)
            # Set stop event
            stop_event.set()
            print("Motion stopped")
        else:
            print("Invalid command, please try again")


if __name__ == "__main__":
    rpc_cli = RpcClient()
    # Set RPC timeout
    rpc_cli.setRequestTimeout(1000)
    # Connect to RPC service
    rpc_cli.connect(LOCAL_IP, 30004)
    # Login to RPC service
    rpc_cli.login("aubo", "123456")

    # Create stop event
    stop_event = threading.Event()

    # Create and start motion control and operation control threads
    motion_thread = threading.Thread(target=robot_motion_control, args=(rpc_cli, ))
    control_thread = threading.Thread(target=control_operations, args=(rpc_cli, ))

    motion_thread.start()
    control_thread.start()

    # Wait for threads to finish
    motion_thread.join()
    control_thread.join()

    # Logout and disconnect
    rpc_cli.logout()
    rpc_cli.disconnect()
