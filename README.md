# object-follower-car
Code for a basic car that follows a particular object after detecting it on the camera

## Getting Started
### Prerequisites
#### Hardware requirements
- A car needs to be modified by attaching batteries and microcontrollers in order to support commands from this interface
- Jetson Development Kit (TX2, Xavier, etc) along with accessories such as Display, Keyboard, Mouse
- A camera for detecting the object (preferably zed camera)
- Xbox Joystick (to control the car manually, if needed)
- USB hub
#### Software requirements
- Latest version of Jetpack installed on the Jetson development kit along with OS and libraries such as TensorRT, CUDA, CuDNN
- Appropriate version of ROS ([Kinetic](https://www.jetsonhacks.com/2018/04/27/robot-operating-system-ros-on-nvidia-jetson-tx-development-kits/)/[Melodic](http://wiki.ros.org/melodic/Installation/Ubuntu))
- [Jetson Utils ROS implementation](https://github.com/dusty-nv/ros_deep_learning) and all its requirements
- [ZED SDK](https://www.stereolabs.com/developers/release/)
- [ZED ROS wrapper](https://github.com/stereolabs/zed-ros-wrapper)

### Installation
Clone this repository to any desired location on your system:
```
git clone https://github.com/theparselmouth/object-follower-car.git
```
Navigate to the ros_deep_learning/src folder that will be in your catkin workspace once you clone the ROS implementation of jetson Utils. Copy all the files downloaded/cloned from this repo into this src folder.
After the workspace has been created, open a terminal and execute the following statement:
```
./bashrc
```
In the window that opens, navigate to the end and add the following line:
```
source ~/catkin_ws/devel/setup.bash
```
Save and close the window
## Usage
### Giving execution permission 
Before running the interface for the first ever time, execute the following commands one by one in a terminal window:
```
chmod +x ~/catkin_ws/src/ros_deep_learning/src/get_image.py
```
```
chmod +x ~/catkin_ws/src/ros_deep_learning/src/runner.py
```
This needs to be done only once before the first ever time the interface is run
### Connecting the hardware
Connect the Joystick, camera to the Jetson development kit 
### Running the interface
To run the interface simply navigate to the ros_deep_learning/src folder in your catkin workspace and run the following the command:
```
bash run_interface.sh
```
The interface runs by default for a network that detects bottles which can be changed to any of the other available neural networks or even a neural network that was trained by the user via the digits server
### Structure of the interface
The following image depicts the structure of the interface

![Alt text](structure.png?raw=true "Interface Structure")

### Checking object detection frequency
To check the frequency at which the neural network detects objects in images, go to the terminal window where the runner.py file is running. Here the first parameter of each line will be the time elapsed from the start of execution. The time difference between consecutive detections will you give you an idea of the frequency of the detection
