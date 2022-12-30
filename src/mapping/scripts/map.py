#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Pose, Point, Quaternion
from nav_msgs.msg import Odometry
import math
from math import radians
import tf
import tf2_ros
import numpy as np


class OccupancyMap:
    def __init__(self):
        # get the positionof robot_odom using tf
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer)
        # Subscribe to rear laser topic
        self.laser = rospy.Subscriber("/scan_multi", LaserScan, callback = self.laserCallback ,queue_size=1)
        # Subscribe to odom topic
        self.odom = rospy.Subscriber("/robot/robotnik_base_control/odom", Odometry, callback = self.odomCallback ,queue_size=1)
        # Publish the occupancy map
        self.occupancyMap = rospy.Publisher("/occupancy_map", OccupancyGrid, queue_size=1)
        self.laserData = LaserScan()
        # Set the initial position of the robot
        self.odomData = Odometry()
        # Create an occupancy grid
        self.occupancyGrid = OccupancyGrid()
        self.occupancyGrid.header.stamp = rospy.Time.now()
        # Set the header of the occupancy grid
        self.occupancyGrid.header.frame_id = "robot_map"
        # Set the resolution of the occupancy grid
        self.occupancyGrid.info.resolution = 0.2
        # Set the width of the occupancy grid
        self.occupancyGrid.info.width = int(1000)
        # Set the height of the occupancy grid
        self.occupancyGrid.info.height = int(1000)
        # make the origin centered
        # [0.030, -0.032, 0.000]
        # xo, yo, zo = self.tfBuffer.lookup_transform("robot_map", "robot_odom", rospy.Time()).transform.translation
        self.occupancyGrid.info.origin.position.x = 0.03 - self.occupancyGrid.info.resolution * self.occupancyGrid.info.width/2
        self.occupancyGrid.info.origin.position.y = -0.032 - self.occupancyGrid.info.resolution * self.occupancyGrid.info.height/2
        self.occupancyGrid.info.origin.position.z = 0
        self.occupancyGrid.info.origin.orientation.x = 0
        self.occupancyGrid.info.origin.orientation.y = 0
        self.occupancyGrid.info.origin.orientation.z = 0
        self.occupancyGrid.info.origin.orientation.w = 1
        # set the size of the occupancy grid
        self.occupancyGrid.data = [-1]* self.occupancyGrid.info.width * self.occupancyGrid.info.height
        self.hits = np.zeros(self.occupancyGrid.info.width * self.occupancyGrid.info.height)
        self.missed = np.ones(self.occupancyGrid.info.width * self.occupancyGrid.info.height)
    def laserCallback(self,msg):
        self.laserData = msg
    def odomCallback(self,msg):
        self.odomData = msg
    def isInsideMap(self, x, y):
        w = self.occupancyGrid.info.width/self.occupancyGrid.info.resolution
        h = self.occupancyGrid.info.height/self.occupancyGrid.info.resolution
        if x < 0 or x >= w or y < 0 or y >= h:
            return False
        return True
    def getRayEnd(self, x, y, theta, r):
        # r/=self.occupancyGrid.info.resolution
        x = x + r * math.cos(theta)
        y = y + r * math.sin(theta)
        return x, y
    def positionToMap(self, x, y):
        robotX = x - self.occupancyGrid.info.resolution * self.occupancyGrid.info.width/2
        robotX /= self.occupancyGrid.info.resolution 
        robotY = y - self.occupancyGrid.info.resolution * self.occupancyGrid.info.height/2
        robotY /= self.occupancyGrid.info.resolution
        return robotX, robotY
    def reflection_model(self):
        if self.laserData.ranges == []:
            return
        # Get robot position
        robotX, robotY = self.positionToMap(self.odomData.pose.pose.position.x, self.odomData.pose.pose.position.y)
        robotOrientationQuaternion = self.odomData.pose.pose.orientation
        _,_,robotOrientation  = tf.transformations.euler_from_quaternion([robotOrientationQuaternion.x, robotOrientationQuaternion.y, robotOrientationQuaternion.z, robotOrientationQuaternion.w])
        # get array of angles from 0 to 360 with step 0.5 degrees
        angles = np.arange(0, 2 * math.pi, 0.5 * math.pi / 180) 
        ranges = list(self.laserData.ranges) # cast self.laserData.ranges to list
        for i in range(len(self.laserData.ranges)):
            if ranges[i] >=30 or ranges[i] <= 0.08: # if the range is out of the laser range
                continue
            try:
                distance = ranges[i] / self.occupancyGrid.info.resolution
                angle = angles[i] + robotOrientation + radians(180)
                # rospy.loginfo("angle: %f", rospy.rostime.Time().now().to_sec())
                endX, endY = self.getRayEnd(robotX, robotY, angle, distance) 
                # rospy.loginfo("endX: %f, endY: %f", endX, endY)
                # if self.isInsideMap(endX, endY):
                #     rospy.loginfo("not inside map")
                #     continue
                index = int(endY) * self.occupancyGrid.info.width + int(endX)
                # check if index is inside the map
                # if abs(index) >= len(self.occupancyGrid.data):
                #     rospy.loginfo(index)
                #     continue
                self.hits[index] += 1 # increment the hit counter of the end point of the ray
                # self.missed[index] -= 1 # decrement the missed counter of the end point of the ray
                # calculate the points between the start and end points of the ray
                dx = (endX - robotX) / distance
                dy = (endY - robotY) / distance 
                xs = np.arange(robotX, endX+dx, dx).astype(int)
                ys = np.arange(robotY, endY+dy, dy).astype(int)
                minLen = min(len(xs), len(ys))
                xs = xs[:minLen]
                ys = ys[:minLen]
                # increment the missed counter of the points between the start and end points of the ray
                self.missed[ys * self.occupancyGrid.info.width + xs] += 1
                # self.missed[ys * self.occupancyGrid.info.width + xs] = np.clip(self.missed[ys * self.occupancyGrid.info.width + xs], 1, 100)
            except Exception as e:
                rospy.loginfo(e)
                continue
    
        # Map the values of hits and missed to the range [0, 100]
        self.hits = (self.hits - np.min(self.hits)) / (np.max(self.hits) - np.min(self.hits)) * 100 + 1
        self.missed = (self.missed - np.min(self.missed)) / (np.max(self.missed) - np.min(self.missed)) * 100 +1
        # print min and max of hits and missed
        rospy.loginfo("min hits: %f, max hits: %f", np.min(self.hits), np.max(self.hits))  
        rospy.loginfo("min missed: %f, max missed: %f", np.min(self.missed), np.max(self.missed))
        prob = (self.hits / (self.hits + self.missed)) * 100
        prob = prob.astype(int).flatten().tolist()
        # print min and max of prob
        rospy.loginfo("min prob: %f, max prob: %f", np.min(prob), np.max(prob))
        self.occupancyGrid.data = [x for x in prob if x != 0]
        # Publish the occupancy grid
        self.occupancyMap.publish(self.occupancyGrid)

        

        

if __name__ == '__main__':
    rospy.init_node('occupancy_map')
    rospy.loginfo('Occupancy map node started')
    rate = rospy.Rate(2)
    occupancyMap = OccupancyMap()
    while not rospy.is_shutdown():
        occupancyMap.reflection_model()
        rate.sleep()
    rospy.spin()
