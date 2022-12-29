#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Pose, Point, Quaternion
from nav_msgs.msg import Odometry
import math
import tf
import numpy as np


class OccupancyMap:
    def __init__(self):
        # Subscribe to rear laser topic
        self.rearLaser = rospy.Subscriber("/robot/rear_laser/scan", LaserScan, callback = self.rearLaserCallback ,queue_size=10)
        # Subscribe to odom topic
        self.odom = rospy.Subscriber("/robot/robotnik_base_control/odom", Odometry, callback = self.odomCallback ,queue_size=10)
        # Publish the occupancy map
        self.occupancyMap = rospy.Publisher("/occupancy_map", OccupancyGrid, queue_size=10)
        self.rearLaserData = LaserScan()
        # Set the initial position of the robot
        self.odomData = Odometry()
        # Create an occupancy grid
        self.occupancyGrid = OccupancyGrid()
        self.occupancyGrid.header.stamp = rospy.Time.now()
        # Set the header of the occupancy grid
        self.occupancyGrid.header.frame_id = "robot_map"
        # Set the width of the occupancy grid
        self.occupancyGrid.info.width = 100
        # Set the height of the occupancy grid
        self.occupancyGrid.info.height = 100
        # Set the resolution of the occupancy grid
        self.occupancyGrid.info.resolution = 0.2
        # make the origin centered
        self.occupancyGrid.info.origin.position.x = -10
        self.occupancyGrid.info.origin.position.y = -10
        self.occupancyGrid.info.origin.position.z = 0
        self.occupancyGrid.info.origin.orientation.x = 0
        self.occupancyGrid.info.origin.orientation.y = 0
        self.occupancyGrid.info.origin.orientation.z = 0
        self.occupancyGrid.info.origin.orientation.w = 1
        # set the size of the occupancy grid
        self.occupancyGrid.data = [-1]* self.occupancyGrid.info.width * self.occupancyGrid.info.height
        self.hits = [1] * self.occupancyGrid.info.width * self.occupancyGrid.info.height
        self.missed= [1] * self.occupancyGrid.info.width * self.occupancyGrid.info.height
    def rearLaserCallback(self,msg):
        self.rearLaserData = msg
        # trasnform the laser scan data to the map frame
        self.rearLaserData.header.frame_id = "robot_map"
    def odomCallback(self,msg):
        self.odomData = msg

    def reflection_model(self):
        if self.rearLaserData.ranges == []:
            return
            
        # Get robot position
        robotX = self.odomData.pose.pose.position.x
        robotY = self.odomData.pose.pose.position.y
        # Get robot orientation
        robotOrientation = self.odomData.pose.pose.orientation
        # iterate over the map 
        for i in range(self.occupancyGrid.info.width):
            for j in range(self.occupancyGrid.info.height):
                # Get the position of the cell
                cellX = self.occupancyGrid.info.origin.position.x + i * self.occupancyGrid.info.resolution
                cellY = self.occupancyGrid.info.origin.position.y + j * self.occupancyGrid.info.resolution
                # Get the distance between the robot and the cell
                distance = math.sqrt((cellX - robotX)**2 + (cellY - robotY)**2)
                # Get the angle between the robot and the cell
                angle = math.atan2(cellY - robotY, cellX - robotX)
                # Get the angle between the robot orientation and the cell
                angle = angle - tf.transformations.euler_from_quaternion([robotOrientation.x, robotOrientation.y, robotOrientation.z, robotOrientation.w])[2]
                # convert the angle to degrees
                angle_d = angle * 180 / math.pi
                # angle should be between -135 and 135
                angle_d %= 360
                # if the angle is out of range, skip the cell
                if angle_d < -135 or angle_d > 135:
                    continue
                rotaionOffset = -270
                # map -135 and 135 to -45 and 45
                angle_d += rotaionOffset 
                # get the index of the angle in the list
                index = int((angle_d + (135 - rotaionOffset)) / 0.5)
                # Check if the cell is in the laser scan data
                if index < len(self.rearLaserData.ranges) and index >= 0:
                    laserDistance = self.rearLaserData.ranges[index]
                    # Check if the cell is in the laser scan range
                    if abs(laserDistance - distance) < 0.1:
                        self.hits[i * self.occupancyGrid.info.width + j] += 1
                    else:
                        self.missed[i * self.occupancyGrid.info.width + j] += 20
                else:
                    logMsg = "index out of range. Index = " + str(index) + ", angle = " + str(angle_d)
                    rospy.loginfo(logMsg)
        # Print hits and missed
        rospy.loginfo("hits = " + str(self.hits))
        # rospy.loginfo("missed = " + str(self.missed))            
        # Update the occupancy grid data
        for i in range(self.occupancyGrid.info.width * self.occupancyGrid.info.height):
            if self.hits[i] > 0 and  self.missed[i] > 0:
                self.occupancyGrid.data[i] = int(self.hits[i] / (self.hits[i] + self.missed[i]))
            # else:
            #     self.occupancyGrid.data[i] = 0
        # if the value of the cell is less than  1/10 from the maximum value, set it to 0
        # maxVal = max(self.occupancyGrid.data)
        # for i in range(self.occupancyGrid.info.width * self.occupancyGrid.info.height):
        #     if maxVal - self.occupancyGrid.data[i]  < 1:
        #         self.occupancyGrid.data[i] = 0
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
