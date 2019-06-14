#!/bin/bash

echo "Starting roscore..."
gnome-terminal -e "roscore"
echo "done!"
sleep 5
echo "Registering joystick..."
gnome-terminal -e "sudo xboxdrv --silent"
echo "done!"
sleep 5
echo "Starting joystick node..."
gnome-terminal -e "rosrun joy joy_node"
echo "done!"
sleep 5
echo "Starting ZED node..."
gnome-terminal -e "roslaunch zed_wrapper zed.launch"
echo "Done!"
sleep 5
echo "Starting get_image.py..."
gnome-terminal -e "rosrun ros_deep_learning get_image.py"
echo "Done!"
sleep 5
echo "Starting detectnet..."
gnome-terminal -e "rosrun ros_deep_learning detectnet /detectnet/image_in:=image_topic_l_publisher _model_name:=coco-bottle"
echo "Done!"
sleep 5
echo "Starting controller..."
gnome-terminal -e "rosrun ros_deep_learning runner.py"
echo "Done!"
sleep 5
echo "Starting depth inference..."
gnome-terminal -e "roslaunch /home/nvidia/catkin_ws/src/stereo_dnn_ros/launch/ResNet18_2D_fp32.launch"
echo "Done!"