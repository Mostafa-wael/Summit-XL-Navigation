#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
# import custom message sensor_out.msg
from sensor_out.msg import SensorOut

# def rearLaserCallback(msg):
#     # Print the data
#     rospy.loginfo("Rear Laser")
# def frontLaserCallback(msg):
#     # Print the data
#     rospy.loginfo("Front Laser")
# def odomCallback(msg):
#     # Print the data
#     rospy.loginfo("Odom")
# if __name__ == '__main__':
#     rospy.init_node("Summit_XL_Sensor")
#     rospy.loginfo("Summit XL Sensor Started")
#     # Define a specific rate to send commands
#     rate = rospy.Rate(2)
#     while not rospy.is_shutdown():
#         # Subscribe to /robot/rear_laser/scan topic
#         rearLaser = rospy.Subscriber("/robot/rear_laser/scan", LaserScan, callback = rearLaserCallback, queue_size=10)
#         # Subscribe to /robot/front_laser/scan topic
#         frontLaser = rospy.Subscriber("/robot/front_laser/scan", LaserScan, callback = frontLaserCallback, queue_size=10)
#         # Subscribe to /robot/robotnik_base_control/odom topic
#         odom = rospy.Subscriber("/robot/robotnik_base_control/odom", Odometry, callback = odomCallback, queue_size=10)
#         rate.sleep()
# Create a sensor class
class Sensor:
    def __init__(self):
        # Define a specific rate to send commands
        self.rate = rospy.Rate(2)
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
    def frontLaserCallback(self,msg):
        self.frontLaserData = msg
    def odomCallback(self,msg):
        self.odomData = msg
    def combineLaserData(self):
        combinedLaserData = LaserScan()
        if self.rearLaserData == None or self.frontLaserData == None:
            rospy.loginfo('No data')
            pass
        else:
            combinedLaserData.header.seq = self.rearLaserData.header.seq
            combinedLaserData.header.stamp = self.rearLaserData.header.stamp
            combinedLaserData.header.frame_id = self.rearLaserData.header.frame_id
            combinedLaserData.angle_min = self.rearLaserData.angle_min
            combinedLaserData.angle_max = self.rearLaserData.angle_max + -(self.frontLaserData.angle_min) + self.frontLaserData.angle_max
            combinedLaserData.angle_increment = self.rearLaserData.angle_increment
            combinedLaserData.time_increment = self.rearLaserData.time_increment
            combinedLaserData.scan_time = self.rearLaserData.scan_time
            combinedLaserData.range_min = self.rearLaserData.range_min
            combinedLaserData.range_max = self.rearLaserData.range_max
            combinedLaserData.ranges = self.rearLaserData.ranges + self.frontLaserData.ranges
            combinedLaserData.intensities = self.rearLaserData.intensities
        return combinedLaserData
    def run(self):
        while not rospy.is_shutdown():
            combinedLaserData = self.combineLaserData()
            
            self.rate.sleep()
if __name__ == '__main__':

    rospy.init_node("Summit_XL_Sensor")
    rospy.loginfo("Summit XL Sensor Started")

    sensor = Sensor()
    sensor.run()

    rospy.spin()