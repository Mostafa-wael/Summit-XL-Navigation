#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from sensor.msg import CombinedSensor
import  message_filters


class Sensor:
    def __init__(self):
        self.sensorsData = CombinedSensor()   
        # set the header of the combined sensor data
        self.sensorsData.header.frame_id = "robot_map" 
        self.sensorsData.header.stamp = rospy.Time.now()
        # create a publisher
        self.sensorPub = rospy.Publisher("/sensors", CombinedSensor, queue_size=1)
        # Subscribe to rear laser topic
        self.laser = message_filters.Subscriber("/scan_multi", LaserScan)
        # Subscribe to odom topic
        self.odom = message_filters.Subscriber("/robot/robotnik_base_control/odom", Odometry)
        # define the approximate time synchronizer
        self.synchronizer = message_filters.ApproximateTimeSynchronizer([self.laser, self.odom], 1, 0.0001)
        self.synchronizer.registerCallback(self.sensorCallback)
    def sensorCallback(self, laserData, odomData):
        # save the data
        self.sensorsData.laser = laserData
        self.sensorsData.odom = odomData
        # publish the combined sensor data
        self.sensorPub.publish(self.sensorsData)


if __name__ == '__main__':
    rospy.init_node('sensors')
    rospy.loginfo('sensor node started')
    rate = rospy.Rate(2)
    sensor = Sensor()
    while not rospy.is_shutdown():
        rate.sleep()
    rospy.spin()