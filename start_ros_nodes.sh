#!/bin/bash

# Source the core ROS2 environment
source /opt/ros/jazzy/setup.bash

# Source the vision workspace
source /home/floatbot/floatbot-vision/install/setup.bash

# Execute vision launch file
ros2 launch floatbot_vision vision.launch.py