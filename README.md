## How to ...
### How to launch Gazebo + rViz
``` bash
roslaunch summit_xl_sim_bringup summit_xls_complete.launch
```
### How to list ROS topics related to robot movement commands
``` bash
rostopic list | grep cmd_vel
```
Note: that you should be running the simulator since that's what publishes to
the topic.

### How to Control robot movement
``` bash
rosrun teleop_twist_keyboard teleop_twist_keyboard.py /cmd_vel:=/robot/robotnik_base_control/cmd_vel
```
### How to run a node
``` bash
rosrun <package_name> <script_name>.py
```
example:
``` bash
rosrun sensor sensor.py
```
### How to create a new package
``` bash
catkin_create_pkg <package_name> [depend1] [depend2] [depend3]
mkdir -p <package_name>/scripts
touch <package_name>/scripts/<script_name>.py
```
example:
``` bash
catkin_create_pkg sensor rospy 
mkdir -p sensor/scripts
touch sensor/scripts/sensor.py
```
```
### How to create and add new messgaes
Follow the instructions in the [ROS wiki](http://wiki.ros.org/ROS/Tutorials/CreatingMsgAndSrv)