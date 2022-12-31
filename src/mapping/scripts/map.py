#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Pose, Point, Quaternion
from nav_msgs.msg import Odometry
from sensor.msg import CombinedSensor
import math
from math import radians
import tf
import tf2_ros
import numpy as np


class OccupancyMap:
    def __init__(self):
        # TODO: use /tf to get the position of the robot in the map
        # Subscribe to the sensors topic
        self.sensor = rospy.Subscriber("/sensors", CombinedSensor, callback = self.sensorCallback ,queue_size=1)
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
        # save old data
        self.prevX, self.prevY, self.prevTheta = self.getPose(knownPose = True)
        # self.prevX = self.positionToMap(self.odomData.pose.pose.position.x, self.odomData.pose.pose.position.y)[0]
        # self.prevY = self.positionToMap(self.odomData.pose.pose.position.x, self.odomData.pose.pose.position.y)[1]
        # self.prevTheta = tf.transformations.euler_from_quaternion([
        #         self.odomData.pose.pose.orientation.x, self.odomData.pose.pose.orientation.y, 
        #         self.odomData.pose.pose.orientation.z, self.odomData.pose.pose.orientation.w])[2]
        self.prevTime = self.odomData.header.stamp
        
    def sensorCallback(self,msg):
        self.laserData = msg.laser
        self.odomData = msg.odom
        self.getPose(knownPose=False)
    def isInsideMap(self, x, y):
        w = self.occupancyGrid.info.width/self.occupancyGrid.info.resolution
        h = self.occupancyGrid.info.height/self.occupancyGrid.info.resolution
        if x < 0 or x >= w or y < 0 or y >= h:
            return False
        return True
    def getRayEnd(self, x, y, theta, r):
        x = x + r * math.cos(theta)
        y = y + r * math.sin(theta)
        return x, y
    def positionToMap(self, x, y):
        # x = x - self.occupancyGrid.info.origin.position.x
        # y = y - self.occupancyGrid.info.origin.position.y
        robotX = x - self.occupancyGrid.info.resolution * self.occupancyGrid.info.width/2
        robotX /= self.occupancyGrid.info.resolution 
        robotY = y - self.occupancyGrid.info.resolution * self.occupancyGrid.info.height/2
        robotY /= self.occupancyGrid.info.resolution
        return robotX, robotY
    def getPose(self, knownPose):
        if knownPose:
            robotX, robotY = self.positionToMap(self.odomData.pose.pose.position.x, self.odomData.pose.pose.position.y)
            robotOrientation  = tf.transformations.euler_from_quaternion([
                self.odomData.pose.pose.orientation.x, self.odomData.pose.pose.orientation.y, 
                self.odomData.pose.pose.orientation.z, self.odomData.pose.pose.orientation.w])[2]
        else:
            vX = self.odomData.twist.twist.linear.x / self.occupancyGrid.info.resolution
            vY = self.odomData.twist.twist.linear.y / self.occupancyGrid.info.resolution
            vTheta = self.odomData.twist.twist.angular.z 
            dt = (self.odomData.header.stamp - self.prevTime).to_sec()
            # print the previous data
            # rospy.loginfo("prevX: %f, prevY: %f, prevTheta: %f", self.prevX, self.prevY, self.prevTheta)
            # rospy.loginfo("vX: %f, vY: %f, vTheta: %f", vX, vY, vTheta)
            # rospy.loginfo("dt: %f", dt)
            # calc the new position based on the velocity
            robotOrientation = self.prevTheta + vTheta * dt
            avgTheta = ((self.prevTheta + robotOrientation)/2) % (2*math.pi)
            robotX = self.prevX + vX * dt * math.cos(avgTheta) - vY * dt * math.sin(avgTheta)
            robotY = self.prevY + vX * dt * math.sin(avgTheta) + vY * dt * math.cos(avgTheta)
            # save the new position
            self.prevX = robotX
            self.prevY = robotY
            self.prevTheta = robotOrientation
            self.prevTime = self.odomData.header.stamp
            # TODO: correction step, using ekf or kf
        return robotX, robotY, robotOrientation
    def reflection_model(self):
        if self.laserData.ranges == []:
            return
        robotX, robotY, robotOrientation = self.getPose(knownPose = True)
        real_robotX, real_robotY, real_robotOrientation = self.getPose(knownPose=False)
        rospy.loginfo("------------------------------------")
        rospy.loginfo("robotX: %f, robotY: %f, robotOrientation: %f", robotX, robotY, robotOrientation)
        rospy.loginfo("real_robotX: %f, real_robotY: %f, real_robotOrientation: %f", real_robotX, real_robotY, real_robotOrientation)
        # log the difference between the real position and the estimated position
        rospy.loginfo("diffX: %f, diffY: %f, diffTheta: %f", real_robotX - robotX, real_robotY - robotY, real_robotOrientation - robotOrientation)
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
        try:
            # Map the values of hits and missed to the range [1, 101]
            self.hits = (self.hits - np.min(self.hits)) / (np.max(self.hits) - np.min(self.hits)) * 100 + 1
            self.missed = (self.missed - np.min(self.missed)) / (np.max(self.missed) - np.min(self.missed)) * 100 +1
            # print min and max of hits and missed
            # rospy.loginfo("min hits: %f, max hits: %f", np.min(self.hits), np.max(self.hits))  
            # rospy.loginfo("min missed: %f, max missed: %f", np.min(self.missed), np.max(self.missed))
            prob = (self.hits / (self.hits + self.missed)) 
            # Normalize the values of prob to the range [0, 100]
            prob = (prob - np.min(prob)) / (np.max(prob) - np.min(prob)) * 100
            prob = prob.astype(int).flatten().tolist()
            # print min and max of prob
            # rospy.loginfo("min prob: %f, max prob: %f", np.min(prob), np.max(prob))
            self.occupancyGrid.data = [x if x !=0 else -1 for x in prob]
            # Publish the occupancy grid
        except Exception as e:
            rospy.loginfo(e)
            return

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


# TODO: we should subtract the origin of the robot in each step we divide by resolution