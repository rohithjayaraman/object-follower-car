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


## Features and their implementation
### Neural Network for detection
The neural network used was the detectnet network that is built by default as part of the [jetson inference](https://github.com/dusty-nv/jetson-inference) repo. The ros_detectnet.cpp file has been modified. Originally, it published to a rostopic with a 2-D array with the coordinates which was modified so that the program now publishes a string with the coordinates, confidence of detection of the bounding box. The neural network used for this program was the 'coco-bottle' network that is a pretrained network available via jetson-inference. This can be substituted with any other network in the available list or a new network can be trained on the digits server 

### Checking object detection frequency
To check the frequency at which the neural network detects objects in images, go to the terminal window where the runner.py file is running. Here the first parameter of each line will be the time elapsed from the start of execution. The time difference between consecutive detections will you give you an idea of the frequency of the detection

### Image type conversion
The ZED node retrieves the image from the camera in a format that cannot be processed directly by the neural network. So we require an image converter that can convert from the image type given by the ZED to the image type that is required for the detection neural network. The python script-ROS node called get_image.py does exactly this 

### Target and Actual steer, throttle
The characteristics of the car are represented by its steer and throttle. Now there are two values for each of these namely the target value and actual value. The target value is the value that needs to be achieved, the value that is the limit (in order to ensure that the value is within control). The actual value is the current steer or throttle value of the car. The actual value is increased or decreased by 1 based on what the target value is

### Kalman Filter
A kalman filter was used to smoothen the value of the calculated distance between the car and the object. A one variable kalman filter was used and the constant that is used to calculate the distance from the object is specific to a bottle(of approximate height 20cm). For a different object the constant must be modified appropriately 

### Switch between manual and automatic mode
By default, the car runs automatically. It detects an object and moves towards it by steering towards it until it is within 25 cm of the object. There is an additional feature which allows the user to manually control the car in case it is needed. Once the joystick is connected, simply press the LB button to switch the control to manual mode. Now the X,Y,A,B buttons can be used to modify the target values. The left and right sticks of the joystick can be used to modify the actual values of the car. The power button can be pressed in order to stop the car immediately (more like a Emergency stop button). The back button can be used to switch back to automatic control mode
