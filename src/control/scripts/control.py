#!/usr/bin/env python3

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
import sys
import tty
import termios
from select import select


# define control class
class Control:
    def __init__(self):
        # define the timeout for the key
        self.key_timeout = 0.5
        # Create a publisher to send commands to the summit_xl
        self.controlPub = rospy.Publisher("/robot/robotnik_base_control/cmd_vel", Twist, queue_size=10)
        self.twist = Twist()

    def getTermianlSettings(self):
        # get the terminal settings
        return termios.tcgetattr(sys.stdin)

    def restoreTerminalSettings(self, settings):
        # restore the terminal settings
        return termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    def getPressedChar(self, settings,timeout):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select([sys.stdin], [], [], timeout)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key
    # Control the robot with WASD keys , if the key is pressed, the robot will move 
    def handleMotion(self):
        settings = self.getTermianlSettings()
        key = self.getPressedChar(settings, self.key_timeout)
        try:
            # if w is pressed, the robot will move forward and increase the linear velocity
            if key == 'w':
                self.twist.linear.x += 0.1
            # if s is pressed, the robot will move backward and decrease the linear velocity
            elif key == 's':
                self.twist.linear.x -= 0.1
            # if a is pressed, the robot will move left and increase the angular velocity
            elif key == 'a':
                self.twist.angular.z += 0.1
            # if d is pressed, the robot will move right and decrease the angular velocity
            elif key == 'd':
                self.twist.angular.z -= 0.1
            # else decrease the linear and angular velocity until it reaches 0
            else:
                self.twist.linear.x *= 0.1
                self.twist.angular.z *= 0.1
            # publish the command to the robot
            self.controlPub.publish(self.twist)
        finally:
            self.restoreTerminalSettings(settings)


if __name__ == '__main__':
    rospy.init_node("Controller")
    rospy.loginfo("Summit XL Controller Started")
    # Define a specific rate to send commands
    rate = rospy.Rate(50)
    # Create an object from the control class
    control = Control()
    while not rospy.is_shutdown():
        # call the handleMotion function
        control.handleMotion()
        rate.sleep()
    rospy.spin()
       

