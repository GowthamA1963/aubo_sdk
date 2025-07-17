#! /usr/bin/env python
# coding=utf-8

"""
Stress Test (Thread-Safe Version)
- readTest(): 10 threads continuously get TCP offset (for N seconds)
- connectTest(): 10 threads continuously connect and disconnect (for N seconds)
"""

import pyaubo_sdk
import time
import threading

robot_ip = "192.168.0.141"
robot_port = 30004
USERNAME = "aubo"
PASSWORD = "123456"

RUN_DURATION = 10  # Duration to run each test in seconds
NUM_THREADS = 10   # Number of threads to spawn


def read_thread(stop_event, thread_id):
    client = pyaubo_sdk.RpcClient()
    try:
        client.connect(robot_ip, robot_port)
        client.login(USERNAME, PASSWORD)
        robot_name = client.getRobotNames()[0]
        robot = client.getRobotInterface(robot_name)

        while not stop_event.is_set():
            try:
                robot.getRobotConfig().getTcpOffset()
                print(f"[Read-{thread_id}] ✓", end=' ', flush=True)
                time.sleep(0.01)
            except pyaubo_sdk.AuboException as e:
                print(f"[Read-{thread_id}] ❌ Error: {e}")
    finally:
        client.logout()
        client.disconnect()


def connect_thread(stop_event, thread_id):
    while not stop_event.is_set():
        client = pyaubo_sdk.RpcClient()
        try:
            client.connect(robot_ip, robot_port)
            client.login(USERNAME, PASSWORD)
            print(f"[Conn-{thread_id}] 🔌 Connected", end=' ', flush=True)
            time.sleep(0.01)
            client.logout()
            client.disconnect()
            print(f"[Conn-{thread_id}] 🔌 Disconnected", end=' ', flush=True)
            time.sleep(0.01)
        except pyaubo_sdk.AuboException as e:
            print(f"[Conn-{thread_id}] ❌ Error: {e}")


def read_test():
    print("🧪 Starting readTest()...")
    stop_event = threading.Event()
    threads = []

    for i in range(NUM_THREADS):
        t = threading.Thread(target=read_thread, args=(stop_event, i))
        threads.append(t)
        t.start()

    time.sleep(RUN_DURATION)
    stop_event.set()

    for t in threads:
        t.join()
    print("\n✅ readTest completed.")


def connect_test():
    print("🧪 Starting connectTest()...")
    stop_event = threading.Event()
    threads = []

    for i in range(NUM_THREADS):
        t = threading.Thread(target=connect_thread, args=(stop_event, i))
        threads.append(t)
        t.start()

    time.sleep(RUN_DURATION)
    stop_event.set()

    for t in threads:
        t.join()
    print("\n✅ connectTest completed.")


if __name__ == '__main__':
    # Uncomment whichever test you want to run
    read_test()
    # connect_test()
