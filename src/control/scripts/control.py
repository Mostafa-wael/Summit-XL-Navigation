#!/usr/bin/env python3

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
import sys
import tty
import termios
from select import select

def termianl_settings():
    return termios.tcgetattr(sys.stdin)

def restore_terminal_settings(settings):
    return termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

def get_pressed_char(settings,timeout):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


if __name__ == '__main__':
    rospy.init_node("Summit_XL_Controller")
    rospy.loginfo("Summit XL Controller Started")
    # Create a publisher to send commands to the summit_xl
    pub = rospy.Publisher("/robot/robotnik_base_control/cmd_vel", Twist, queue_size=10)
    # Define a specific rate to send commands
    rate = rospy.Rate(50)
    key_timeout = 0.5
    # Control the robot with WASD keys , if the key is pressed, the robot will move 
    twist = Twist()
    while not rospy.is_shutdown():
        settings = termianl_settings()
        key = get_pressed_char(settings, key_timeout)
        try:
            # if w is pressed, the robot will move forward and increase the linear velocity
            if key == 'w':
                twist.linear.x += 0.5
            # if s is pressed, the robot will move backward and decrease the linear velocity
            elif key == 's':
                twist.linear.x -= 0.5
            # if a is pressed, the robot will move left and increase the angular velocity
            elif key == 'a':
                twist.angular.z += 0.2
            # if d is pressed, the robot will move right and decrease the angular velocity
            elif key == 'd':
                twist.angular.z -= 0.2
            # else decrease the linear and angular velocity until it reaches 0
            else:
                twist.linear.x *= 0.5
                twist.angular.z *= 0.5
            # publish the command to the robot
            pub.publish(twist)
            rate.sleep()
        finally:
            restore_terminal_settings(settings)

