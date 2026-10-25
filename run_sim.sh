#!/usr/bin/env bash
# One command: stop old windows, rebuild, and launch RViz + joint sliders
source /opt/ros/jazzy/setup.bash

pkill -f rviz2 2>/dev/null
pkill -f joint_state_publisher 2>/dev/null
pkill -f robot_state_publisher 2>/dev/null
sleep 1

cd ~/ros2_repaired_ws || exit 1
colcon build --packages-select SimofRack_onlylinear_description 2>&1 | grep -v "naming convention\|lower case\|^---\|stderr" || true
source install/setup.bash

ros2 launch SimofRack_onlylinear_description sliders.launch.py
