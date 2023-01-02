#!/usr/bin/env python3
import numpy as np
import math

import rospy
import tf

from nav_msgs.msg import OccupancyGrid, Odometry
from sensor_msgs.msg import LaserScan
from sensor.msg import CombinedSensor



class Mapper:

    def __init__(self):
        # subscribers
        rospy.Subscriber("/sensors", CombinedSensor, callback = self.sensorCallback ,queue_size=1)
        self.occupancyGridPub = rospy.Publisher("/occupancy_map", OccupancyGrid, queue_size=10)

        # messages
        self.laserData = LaserScan()
        self.odomData = Odometry()
        self.occupancyGrid = OccupancyGrid()

        self.mapWidth = 1000
        self.mapHight = 1000
        self.mapResolution = 0.2
        # maps for hits & missed
        numRows = int(self.mapWidth/self.mapResolution)
        numCols = int(self.mapWidth/self.mapResolution)
        self.hits = np.ones(numRows * numCols)
        self.misses = np.ones(numRows * numCols)
        self.occupancyGrid.data = [-1] * numRows * numCols

        # map metadata
        self.occupancyGrid.header.stamp = rospy.Time.now()
        self.occupancyGrid.header.frame_id = "robot_map"
        self.occupancyGrid.info.width = self.mapWidth
        self.occupancyGrid.info.height = self.mapHight
        self.occupancyGrid.info.resolution = self.mapResolution
        self.occupancyGrid.info.origin.position.x = 0.03 - self.mapWidth*self.mapResolution/2
        self.occupancyGrid.info.origin.position.y = -0.032 - self.mapWidth*self.mapResolution/2
        self.occupancyGrid.info.origin.position.z = 0
        self.occupancyGrid.info.origin.orientation.x = 0
        self.occupancyGrid.info.origin.orientation.y = 0
        self.occupancyGrid.info.origin.orientation.z = 0
        self.occupancyGrid.info.origin.orientation.w = 0

        self.angles = np.arange(0, 2*math.pi, 0.5*math.pi/180)

    def sensorCallback(self, msg):
        self.laserData = msg.laser
        self.odomData = msg.odom

    def getEndFromStart(self, startX, startY, theta, distance):
        endX = startX + math.cos(theta) * distance
        endY = startY + math.sin(theta) * distance
        return (int(endX), int(endY))

    def mapToGrid(self, x, y):
        i = (x - self.occupancyGrid.info.origin.position.x) / self.mapResolution  
        j = (y - self.occupancyGrid.info.origin.position.x) / self.mapResolution  
        return i, j

    def getPose(self):
        x = self.odomData.pose.pose.position.x
        y = self.odomData.pose.pose.position.y
        i, j = self.mapToGrid(x, y)
        theta = tf.transformations.euler_from_quaternion([
            self.odomData.pose.pose.orientation.x, self.odomData.pose.pose.orientation.y,
            self.odomData.pose.pose.orientation.z, self.odomData.pose.pose.orientation.w])[2]

        return i, j, theta

    def buildMap(self):
        if (self.laserData.ranges == []):
            return

        iRobot, jRobot, thetaRobot = self.getPose()
        ranges = list(self.laserData.ranges)
        for i in range(len(ranges)):
            if ranges[i] < self.laserData.range_min or ranges[i] > self.laserData.range_max:
                continue

            distance = ranges[i] / self.mapResolution
            angle = self.angles[i] + thetaRobot + math.pi

            iEnd, jEnd = self.getEndFromStart(iRobot, jRobot, angle, distance)
            self.hits[int(jEnd + self.occupancyGrid.info.width *  iEnd)] += 1

            iStep = (iEnd - iRobot) / distance
            jStep = (jEnd - jRobot) / distance

            iSteps = np.arange(iRobot, iEnd, iStep).astype(int)
            jSteps = np.arange(jRobot, jEnd, jStep).astype(int)
            minLen = min(len(iSteps), len(jSteps))
            iSteps = iSteps[:minLen]
            jSteps = jSteps[:minLen]

            self.misses[jSteps + self.occupancyGrid.info.width * iSteps] += 1

        prob = (self.hits / (self.hits + self.misses)) * 100
        print(prob)
        self.occupancyGrid = prob.flatten().astype(int).tolist()
        self.occupancyGridPub.publish(self.occupancyGrid)

if __name__ == '__main__':
    rospy.init_node("occupancy_map")
    rospy.loginfo('Occupancy map node started')

    mapper = Mapper()
    while not rospy.is_shutdown():
        mapper.buildMap()

    rospy.spin()