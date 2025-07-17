# Aubo SDK Python Examples 🤖

This repository contains Python examples using the Aubo SDK (`pyaubo_sdk`) to control and interact with Aubo collaborative robots.

## 📦 Contents

This SDK version: `0.25.0-rc.4`  
Target robot: **Aubo i-series**  
Communication: RPC over TCP (default port: `30004`)

### 🧪 Examples Included

| Script | Description |
|--------|-------------|
| `example_io.py` | Digital & analog I/O handling (standard + tool) |
| `example_math.py` | Pose math: RPY ⇄ Quaternion, flange ↔ TCP transforms |
| `example_movec.py` | Circular motion using MoveC API |
| `example_movej.py` | Joint motion using MoveJ |
| `example_movel.py` | Linear motion using MoveL |
| `example_force.py` | Get TCP force sensor data (if available) |

## 🚀 Quick Start

1. **Install dependencies**  
   Make sure you have Python 3.7+ and `pyaubo_sdk` installed.

2. **Clone the repo**

   ```bash
   git clone https://github.com/GowthamA1963/aubo_sdk.git
   cd aubo_sdk
Connect the robot to your PC

Ensure both robot and PC are in the same subnet.

You can check your PC's IP using ip a or ipconfig.

Run an example

python share/example/python/example_io.py
⚙️ Configuration
Inside each script, set the correct robot IP:


robot_ip = "192.168.0.xxx"  # Replace with your robot's IP
robot_port = 30004          # Default RPC port
📓 Notes
All motion examples assume the robot is in ready state (no faults).

Use Aubo Studio or hardware pendant to enable servo power before running motion scripts.

The force sensor reading requires a real sensor mounted at the flange or tool.

🧠 Author
Gowtham A
🔗 GitHub

📌 This project is not officially affiliated with Aubo Robotics. For official support, refer to Aubo Robotics.
---

Let me know if you also want:
- a section on how to build the SDK
- or a GIF/image for visualization  
I can generate those too!