## How to run
### Launch Gazebo + rViz
``` bash
roslaunch summit_xl_sim_bringup summit_xls_complete.launch
```
### List ROS topics related to robot movement commands: 
``` bash
rostopic list | grep cmd_vel
```
Note: that you should be running the simulator since that's what publishes to
the topic.

### Control robot movement
``` bash
rosrun teleop_twist_keyboard teleop_twist_keyboard.py /cmd_vel:=/robot/robotnik_base_control/cmd_vel
```
### How to run the control
``` bash
rosrun control control.py
```