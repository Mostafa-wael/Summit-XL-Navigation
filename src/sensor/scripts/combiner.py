#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Pose, Point, Quaternion
from nav_msgs.msg import Odometry
from sensor.msg import CombinedSensor
import math
import  message_filters
from math import radians
import tf
import tf2_ros
import numpy as np


class Sensor:
    def __init__(self):
        self.sensorsData = CombinedSensor()    
        # create a publisher
        self.sensorPub = rospy.Publisher("/sensors", CombinedSensor, queue_size=1)
        # Subscribe to rear laser topic
        self.laser = message_filters.Subscriber("/scan_multi", LaserScan)
        # Subscribe to odom topic
        self.odom = message_filters.Subscriber("/robot/robotnik_base_control/odom", Odometry)
    def sensorCallback(self, laserData, odomData):
        self.sensorsData.laser = laserData
        self.sensorsData.odom = odomData
        self.sensorPub.publish(self.sensorsData)
    def combine(self):
        synchronizer = message_filters.ApproximateTimeSynchronizer([self.laser, self.odom], 1, 0.0001)
        synchronizer.registerCallback(self.sensorCallback)


if __name__ == '__main__':

    rospy.init_node('sensors')
    rospy.loginfo('sensor node started')
    rate = rospy.Rate(2)
    sensor = Sensor()
    while not rospy.is_shutdown():
        sensor.combine()
        rate.sleep()
    rospy.spin()