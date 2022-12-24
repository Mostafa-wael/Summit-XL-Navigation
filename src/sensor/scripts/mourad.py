#!/usr/bin/env python3

import rospy
import roslib
from roslib import message
from sensor_msgs.msg import LaserScan , PointCloud2
from nav_msgs.msg import Odometry
from sensor_msgs import point_cloud2
import tf
from std_msgs.msg import Header

from laser_geometry import LaserProjection

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
        self.listener = tf.TransformBroadcaster()
        self.rearLaserData = LaserScan()
        self.frontLaserData = LaserScan()
        self.odomData = Odometry()
        self.laserProj = LaserProjection()
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
            return None
        else:
            # laser to point cloud
            cloud_out_rear = self.laserProj.projectLaser(self.rearLaserData)
            cloud_out_front = self.laserProj.projectLaser(self.frontLaserData)
            # point cloud to list
            rearLaserPointCloudList = list(point_cloud2.read_points(cloud_out_rear, field_names = ("x", "y", "z"), skip_nans=True))
            frontLaserPointCloudList = list(point_cloud2.read_points(cloud_out_front, field_names = ("x", "y", "z"), skip_nans=True))
            # transform point cloud
            rearLaserPointCloudListTransformed = []
            frontLaserPointCloudListTransformed = []
            for point in rearLaserPointCloudList:
                rearLaserPointCloudListTransformed.append(self.listener.transformPoint("base_link", point))
            for point in frontLaserPointCloudList:
                frontLaserPointCloudListTransformed.append(self.listener.transformPoint("base_link", point))
            # list to point cloud
            rearLaserPointCloud = point_cloud2.create_cloud_xyz32(cloud_out_rear.header, rearLaserPointCloudListTransformed)
            frontLaserPointCloud = point_cloud2.create_cloud_xyz32(cloud_out_front.header, frontLaserPointCloudListTransformed)
            
            # add header
            combinedLaserData.header = self.rearLaserData.header
            # add frame_id
            combinedLaserData.header.frame_id = "base_link"
            combinedLaserData.header.stamp = self.odomData.header.stamp
            combinedLaserData.angle_min = self.rearLaserData.angle_min
            combinedLaserData.angle_max = self.rearLaserData.angle_max
            combinedLaserData.angle_increment = self.rearLaserData.angle_increment
            combinedLaserData.time_increment = self.rearLaserData.time_increment
            combinedLaserData.scan_time = self.rearLaserData.scan_time
            combinedLaserData.range_min = self.rearLaserData.range_min
            combinedLaserData.range_max = self.rearLaserData.range_max
            combinedLaserData.ranges = self.rearLaserData.ranges + self.frontLaserData.ranges
            combinedLaserData.intensities = self.rearLaserData.intensities + self.frontLaserData.intensities


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
