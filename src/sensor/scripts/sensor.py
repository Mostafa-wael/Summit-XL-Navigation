#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
# import custom message sensor_out.msg
# from sensor_out.msg import SensorOut

class Sensor:
    def __init__(self):
        # Subscribe to /robot/rear_laser/scan topic
        self.rearLaser = rospy.Subscriber("/robot/rear_laser/scan", LaserScan, callback = self.rearLaserCallback, queue_size=10)
        # Subscribe to /robot/front_laser/scan topic
        self.frontLaser = rospy.Subscriber("/robot/front_laser/scan", LaserScan, callback = self.frontLaserCallback, queue_size=10)
        # Subscribe to /robot/robotnik_base_control/odom topic
        self.odom = rospy.Subscriber("/robot/robotnik_base_control/odom", Odometry, callback = self.odomCallback, queue_size=10)
        # Create a publisher with a new topic to send laser data
        self.laser = rospy.Publisher("/robot/laser_data", LaserScan, queue_size=10)
        self.rearLaserData = LaserScan()
        self.frontLaserData = LaserScan()
        self.odomData = Odometry()
    def rearLaserCallback(self,msg):
        self.rearLaserData = msg
        rospy.loginfo('Rear laser data angle_min: %f', self.rearLaserData.angle_min * 180 / 3.14159265359)
        rospy.loginfo('Rear laser data angle_max: %f', self.rearLaserData.angle_max * 180 / 3.14159265359)
    def frontLaserCallback(self,msg):
        self.frontLaserData = msg
        rospy.loginfo('Front laser data angle_min: %f', self.frontLaserData.angle_min * 180 / 3.14159265359)
        rospy.loginfo('Front laser data angle_max: %f', self.frontLaserData.angle_max * 180 / 3.14159265359)
    def odomCallback(self,msg):
        self.odomData = msg
    def combineLaserData(self):
        combinedLaserData = LaserScan()
        if self.rearLaserData == None or self.frontLaserData == None:
            rospy.loginfo('No data')
            return None
        else:
            # order doesn't matter
            combinedLaserData.header = self.rearLaserData.header
            combinedLaserData.scan_time = self.rearLaserData.scan_time
            combinedLaserData.time_increment = self.rearLaserData.time_increment
            combinedLaserData.angle_increment = self.rearLaserData.angle_increment
            combinedLaserData.intensities = self.rearLaserData.intensities # always zero
            
            combinedLaserData.range_min = min(self.rearLaserData.range_min, self.frontLaserData.range_min)
            combinedLaserData.range_max = max(self.rearLaserData.range_max, self.frontLaserData.range_max)

            # order matters
            combinedLaserData.angle_min = self.rearLaserData.angle_min + 3.14159265359
            combinedLaserData.angle_max = self.rearLaserData.angle_max - 3.14159265359 
            # print the angle_min and angle_max of the front and rear laser data in degrees
            
            
            # print the angle_min and angle_max of the combined laser data in degrees
            rospy.loginfo('Combined laser data angle_min: %f', combinedLaserData.angle_min * 180 / 3.14159265359)
            rospy.loginfo('Combined laser data angle_max: %f', combinedLaserData.angle_max * 180 / 3.14159265359)
            
            combinedLaserData.ranges = self.rearLaserData.ranges + self.frontLaserData.ranges
            # print the len of the front and rear laser data
            rospy.loginfo('Front laser data len: %d', len(self.frontLaserData.ranges))
            rospy.loginfo('Rear laser data len: %d', len(self.rearLaserData.ranges))
            
        return combinedLaserData
    def publishLaserData(self):
        combinedLaserData = self.combineLaserData()
        if combinedLaserData != None:
            self.laser.publish(combinedLaserData)
            
if __name__ == '__main__':

    rospy.init_node("Summit_XL_Sensor")
    rospy.loginfo("Summit XL Sensor Started")
    # Define a specific rate to send commands
    rate = rospy.Rate(2)
    sensor = Sensor()
    while not rospy.is_shutdown():
        sensor.publishLaserData()
        rate.sleep()
    rospy.spin()