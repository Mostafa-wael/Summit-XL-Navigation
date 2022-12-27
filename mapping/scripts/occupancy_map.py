#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Pose, Point, Quaternion
from nav_msgs.msg import Odometry
import math
import tf


class OccupancyMap:
    def __init__(self):
        # Subscribe to front laser topic
        self.frontLaser = rospy.Subscriber("/robot/front_laser/scan", LaserScan, callback = self.frontLaserCallback ,queue_size=10)
        # Subscribe to odom topic
        self.odom = rospy.Subscriber("/robot/robotnik_base_control/odom", Odometry, callback = self.odomCallback ,queue_size=10)
        # Publish the occupancy map
        self.occupancyMap = rospy.Publisher("/occupancy_map", OccupancyGrid, queue_size=10)
        self.frontLaserData = LaserScan()
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
        self.occupancyGrid.info.origin.position.x = -5
        self.occupancyGrid.info.origin.position.y = -5
        self.occupancyGrid.info.origin.position.z = 0
        self.occupancyGrid.info.origin.orientation.x = 0
        self.occupancyGrid.info.origin.orientation.y = 0
        self.occupancyGrid.info.origin.orientation.z = 0
        self.occupancyGrid.info.origin.orientation.w = 1


        # set the size of the occupancy grid
        self.occupancyGrid.data = [-1]* self.occupancyGrid.info.width * self.occupancyGrid.info.height
        # Initialize the data of the occupancy grid
        self.odomData = Odometry()
    def frontLaserCallback(self,msg):
        self.frontLaserData = msg
    def odomCallback(self,msg):
        self.odomData = msg

    def reflection_model(self):
        if self.frontLaserData.ranges == []:
            return
        rospy.loginfo('Mourad')
        hits = [0] * self.occupancyGrid.info.width * self.occupancyGrid.info.height
        missed= [1] * self.occupancyGrid.info.width * self.occupancyGrid.info.height
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
                # Get the index of the cell in the laser scan data
                index = int(angle / self.frontLaserData.angle_increment)
                # Check if the cell is in the laser scan data
                if index < len(self.frontLaserData.ranges):
                    # Check if the cell is in the laser scan range
                    if self.frontLaserData.ranges[index] > distance - 0.1 and self.frontLaserData.ranges[index] < distance + 0.1:
                        hits[i * self.occupancyGrid.info.width + j] += 1
                    else:
                        missed[i * self.occupancyGrid.info.width + j] += 1
        # Update the occupancy grid data
        for i in range(self.occupancyGrid.info.width * self.occupancyGrid.info.height):
            if hits[i] + missed[i] > 0:
                self.occupancyGrid.data[i] = int(hits[i] * 100 / (hits[i] + missed[i]))
            else:
                self.occupancyGrid.data[i] = -1
        
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
