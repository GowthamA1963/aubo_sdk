#! /usr/bin/env python
# coding=utf-8

"""
Get robot arm IO configuration information

Steps:
Step 1: Connect to the RPC service
Step 2: Robot login
Step 3: Standard Digital IO:
    1. Get the number of standard digital inputs and outputs
    2. Set and get input trigger actions
    3. Set and get output state selection
    4. Get standard digital input and output values
Step 4: Standard Analog IO:
    1. Get the number of standard analog inputs and outputs
    2. Set and get standard analog input range
    3. Get standard analog input
    4. Set and get standard analog output range
    5. Set and get standard analog output state selection
    6. Set and get standard analog output
Step 5: Tool Digital IO
    1. Get the number of tool digital inputs and outputs
    2. Set and get tool digital input trigger actions
    3. Set and get tool digital output state selection
Step 6: Tool Analog IO
    1. Get the number of tool analog inputs and outputs
    2. Get tool analog input range
    3. Get tool analog input
"""

import pyaubo_sdk

robot_ip = "192.168.0.141"  # Server IP address
robot_port = 30004      # Port number
M_PI = 3.14159265358979323846
robot_rpc_client = pyaubo_sdk.RpcClient()


def exampleStandardDigitalIO(robot_name):
    # API call: Get number of standard digital inputs
    input_num = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getStandardDigitalInputNum()
    print("Number of standard digital inputs:", input_num)
    # API call: Get number of standard digital outputs
    output_num = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getStandardDigitalOutputNum()
    print("Number of standard digital outputs:", output_num)

    # API call: Set all input trigger actions to Default
    robot_rpc_client.getRobotInterface(robot_name).getIoControl().setDigitalInputActionDefault()
    # API call: Get input trigger action
    input_action = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getStandardDigitalInputAction(0x00000001)
    print("Input trigger action:", input_action)
    # API call: Get input trigger action
    input_action = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getStandardDigitalInputAction(0x00000001)
    print("Input trigger action:", input_action)

    # API call: Set all output state selection to NONE
    robot_rpc_client.getRobotInterface(robot_name).getIoControl().setDigitalOutputRunstateDefault()
    # API call: Get output state selection
    output_runstate = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getStandardDigitalOutputRunstate(0x00000001)
    print("Output state selection:", output_runstate)

    # API call: Get standard digital output state selection
    output_runstate = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getStandardDigitalOutputRunstate(0x00000001)
    print("Output state selection:", output_runstate)

    # Print all standard digital input values
    input_value = []
    for i in range(input_num):
        value = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getStandardDigitalInput(i)
        input_value.append(value)
    print("Input values:", input_value)

    # Print all standard digital output values
    output_value = []
    for i in range(output_num):
        value = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getStandardDigitalOutput(i)
        output_value.append(value)
    print("Output values:", output_value)


def exampleStandardAnalogIO(robot_name):
    # API call: Get number of standard analog inputs
    input_num = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getStandardAnalogInputNum()
    print("Number of standard analog inputs:", input_num)
    # API call: Get number of standard analog outputs
    output_num = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getStandardAnalogOutputNum()
    print("Number of standard analog outputs:", output_num)

    # API call: Set standard analog input range
    input_domain = 15
    robot_rpc_client.getRobotInterface(robot_name).getIoControl().setStandardAnalogInputDomain(0, input_domain)
    # API call: Get standard analog input range
    input_domain = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getStandardAnalogInputDomain(0)
    print("Standard analog input range:", input_domain)

    # API call: Set standard analog output range
    output_domain = 15
    robot_rpc_client.getRobotInterface(robot_name).getIoControl().setStandardAnalogOutputDomain(0, output_domain)
    # API call: Get standard analog output range
    output_domain = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getStandardAnalogOutputDomain(0)
    print("Standard analog output range:", output_domain)

    # API call: Get standard analog output state selection
    output_runstate = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getStandardAnalogOutputRunstate(3)
    print("Output state selection:", output_runstate)


def exampleToolDigitalIO(robot_name):
    # API call: Get number of tool digital inputs
    input_num = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getToolDigitalInputNum()
    print("Number of tool digital inputs:", input_num)
    # API call: Get number of tool digital outputs
    output_num = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getToolDigitalOutputNum()
    print("Number of tool digital outputs:", output_num)

    # API call: Set specified tool IO as input
    robot_rpc_client.getRobotInterface(robot_name).getIoControl().setToolIoInput(1, True)
    # API call: Check if specified tool IO is input
    isInput = robot_rpc_client.getRobotInterface(robot_name).getIoControl().isToolIoInput(1)
    print("Is specified tool IO input:", isInput)
    # API call: Get tool digital input
    input = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getToolDigitalInput(1)
    print("Tool digital input:", input)

    # API call: Set all tool digital input trigger actions to Default
    input_action = pyaubo_sdk.StandardInputAction.Default
    robot_rpc_client.getRobotInterface(robot_name).getIoControl().setToolDigitalInputAction(0, input_action)
    # API call: Get tool digital input trigger action
    input_action = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getToolDigitalInputAction(0)
    print("Input trigger action:", input_action)

    # API call: Get tool digital output state selection
    output_runstate = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getToolDigitalOutputRunstate(3)
    print("Output state selection:", output_runstate)

    # API call: Set tool digital output
    output = True
    robot_rpc_client.getRobotInterface(robot_name).getIoControl().setToolDigitalOutput(3, output)
    # API call: Get tool digital output
    output = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getToolDigitalOutput(3)
    print("Tool digital output:", output)


def exampleToolAnalogIO(robot_name):
    # API call: Get number of tool analog inputs
    input_num = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getToolAnalogInputNum()
    print("Number of tool analog inputs:", input_num)
    # API call: Get number of tool analog outputs
    output_num = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getToolAnalogOutputNum()
    print("Number of tool analog outputs:", output_num)

    # Loop through all available tool analog input channels
    for i in range(input_num):
        try:
            input_domain = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getToolAnalogInputDomain(i)
            print(f"Tool analog input range ({i}):", input_domain)

            input_value = robot_rpc_client.getRobotInterface(robot_name).getIoControl().getToolAnalogInput(i)
            print(f"Tool analog input ({i}):", input_value)
        except Exception as e:
            print(f"⚠️ Could not read analog input {i}: {e}")



if __name__ == '__main__':
    robot_rpc_client.connect(robot_ip, robot_port)  # API call: Connect to RPC service
    if robot_rpc_client.hasConnected():
        print("Robot rpc_client connected successfully!")
        robot_rpc_client.login("aubo", "123456")  # API call: Robot login
        if robot_rpc_client.hasLogined():
            print("Robot rpc_client logged in successfully!")
            robot_name = robot_rpc_client.getRobotNames()[0]  # API call: Get robot name
            exampleStandardDigitalIO(robot_name)  # Get standard digital IO
            exampleStandardAnalogIO(robot_name)   # Get standard analog IO
            exampleToolDigitalIO(robot_name)      # Get tool digital IO
            exampleToolAnalogIO(robot_name)       # Get tool analog IO
