#!/usr/bin/env python3

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen

if __name__ == '__main__':
    rospy.init_node("Summit_XL_Controller")
    rospy.loginfo("Summit XL Controller Started")
    # Create a publisher to send commands to the summit_xl
    pub = rospy.Publisher("/robot/robotnik_base_control/cmd_vel", Twist, queue_size=10)
    # Define a specific rate to send commands
    rate = rospy.Rate(2)
    # Control the robot with WASD keys , if the key is pressed, the robot will move 
    while not rospy.is_shutdown():
        twist = Twist()
        key = input() # Get the key pressed
        if key == 'w':
            twist.linear.x = 1.0
        elif key == 's':
            twist.linear.x = -1.0
        elif key == 'a':
            twist.angular.z = 1.0
        elif key == 'd':
            twist.angular.z = -1.0
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
        pub.publish(twist)
        rate.sleep()