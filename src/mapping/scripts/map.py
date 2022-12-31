#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from nav_msgs.msg import Odometry
from sensor.msg import CombinedSensor
import math
from math import radians
import tf
import numpy as np


class OccupancyMap:
    def __init__(self, knownPose):
        self.knownPose = knownPose
        # Create a transform listener
        self.listener = tf.TransformListener()
        # Subscribe to the sensors topic
        self.sensor = rospy.Subscriber("/sensors", CombinedSensor, callback = self.sensorCallback ,queue_size=1)
        # Publish the occupancy map
        self.occupancyMap = rospy.Publisher("/occupancy_map", OccupancyGrid, queue_size=1)
        # Create a laser scan
        self.laserData = LaserScan()
        # Create an odometry
        self.odomData = Odometry()
        # Create an occupancy grid
        self.occupancyGrid = OccupancyGrid()
        # Set the header of the occupancy grid
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
        self.occupancyGrid.info.origin.position.x = 0.03 - self.occupancyGrid.info.resolution * self.occupancyGrid.info.width/2
        self.occupancyGrid.info.origin.position.y = -0.032 - self.occupancyGrid.info.resolution * self.occupancyGrid.info.height/2
        self.occupancyGrid.info.origin.position.z = 0
        self.occupancyGrid.info.origin.orientation.x = 0
        self.occupancyGrid.info.origin.orientation.y = 0
        self.occupancyGrid.info.origin.orientation.z = 0
        self.occupancyGrid.info.origin.orientation.w = 1
        # set the size of the occupancy grid
        self.occupancyGrid.data = [-1]* self.occupancyGrid.info.width * self.occupancyGrid.info.height
        self.hits = np.ones(self.occupancyGrid.info.width * self.occupancyGrid.info.height)
        self.missed = np.ones(self.occupancyGrid.info.width * self.occupancyGrid.info.height)
        # save old data
        self.prevX = self.positionToMap(self.odomData.pose.pose.position.x, self.odomData.pose.pose.position.y)[0]
        self.prevY = self.positionToMap(self.odomData.pose.pose.position.x, self.odomData.pose.pose.position.y)[1]
        self.prevTheta = tf.transformations.euler_from_quaternion([
                self.odomData.pose.pose.orientation.x, self.odomData.pose.pose.orientation.y, 
                self.odomData.pose.pose.orientation.z, self.odomData.pose.pose.orientation.w])[2]
        self.prevTime = self.odomData.header.stamp
        
    def sensorCallback(self,msg):
        self.laserData = msg.laser
        self.odomData = msg.odom
        self.getPoseKF()
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
    def getObserved(self):
        robotX, robotY = self.positionToMap(self.odomData.pose.pose.position.x, self.odomData.pose.pose.position.y)
        robotOrientation  = tf.transformations.euler_from_quaternion([
            self.odomData.pose.pose.orientation.x, self.odomData.pose.pose.orientation.y, 
            self.odomData.pose.pose.orientation.z, self.odomData.pose.pose.orientation.w])[2]
        return robotX, robotY, robotOrientation
    def getPredicted(self):
        vX = self.odomData.twist.twist.linear.x / self.occupancyGrid.info.resolution
        vY = self.odomData.twist.twist.linear.y / self.occupancyGrid.info.resolution
        vTheta = self.odomData.twist.twist.angular.z 
        dt = (self.odomData.header.stamp - self.prevTime).to_sec()
        # calc the new position based on the velocity
        robotOrientation = self.prevTheta + vTheta * dt
        robotX = self.prevX + vX * dt * math.cos(robotOrientation) - vY * dt * math.sin(robotOrientation)
        robotY = self.prevY + vX * dt * math.sin(robotOrientation) + vY * dt * math.cos(robotOrientation)
        return robotX, robotY, robotOrientation
    def getPoseTrue(self):
        (x, y, z),(qx, qy, qz, qw) = self.listener.lookupTransform("robot_map", "robot_base_link", rospy.Time(0))
        robotX, robotY = self.positionToMap(x, y)
        robotOrientation  = tf.transformations.euler_from_quaternion([qx, qy, qz, qw])[2]
        return robotX, robotY, robotOrientation
    def getPoseKF(self):
        # get the predicted position
        pred_robotX, pred_robotY, pred_robotOrientation = self.getPredicted()
        # get the observed position
        obs_robotX, obs_robotY, obs_robotOrientation = self.getObserved()
        # get covariance from odom
        covX = self.odomData.pose.covariance[0]
        covY = self.odomData.pose.covariance[7]
        covTheta = self.odomData.pose.covariance[35]
        # get the kalman gain
        kX = 1 # covX / (covX + self.covX)
        kY = 1 # covY / (covY + self.covY)
        kTheta = 1 # covTheta / (covTheta + self.covTheta)
        # update the position
        robotX = pred_robotX + kX * (obs_robotX - pred_robotX)
        robotY = pred_robotY + kY * (obs_robotY - pred_robotY)
        robotOrientation = pred_robotOrientation + kTheta * (obs_robotOrientation - pred_robotOrientation)
        # save the new position
        self.prevX = robotX
        self.prevY = robotY
        self.prevTheta = robotOrientation
        self.prevTime = self.odomData.header.stamp
        return robotX, robotY, robotOrientation
        
    def reflection_model(self):
        if self.laserData.ranges == []:
            return
        if self.knownPose == True:
            robotX, robotY, robotOrientation = self.getPoseTrue()
        else:
            robotX, robotY, robotOrientation = self.getPoseKF()
        # get array of angles from 0 to 360 with step 0.5 degrees
        angles = np.arange(0, 2 * math.pi, 0.5 * math.pi / 180) 
        ranges = list(self.laserData.ranges) # cast self.laserData.ranges to list
        for i in range(len(self.laserData.ranges)):
            if ranges[i] >= self.laserData.range_max or ranges[i] <= self.laserData.range_min: # if the range is out of the laser range
                continue
            try:
                distance = ranges[i] / self.occupancyGrid.info.resolution
                angle = angles[i] + robotOrientation + radians(180)
                endX, endY = self.getRayEnd(robotX, robotY, angle, distance) 
                index = int(endY) * self.occupancyGrid.info.width + int(endX)
                self.hits[index] += 1 # increment the hit counter of the end point of the ray
                # self.missed[index] -= 1 # decrement the missed counter of the end point of the ray

                # calculate the points between the start and end points of the ray
                dx = (endX - robotX) / distance
                dy = (endY - robotY) / distance 
                xs = np.arange(robotX, endX, dx).astype(int)
                ys = np.arange(robotY, endY, dy).astype(int)
                minLen = min(len(xs), len(ys))
                xs = xs[:minLen]
                ys = ys[:minLen]
                # increment the missed counter of the points between the start and end points of the ray
                self.missed[ys * self.occupancyGrid.info.width + xs] += 1
            except Exception as e:
                rospy.loginfo(e)
                continue
    
        prob = (self.hits / (self.hits + self.missed)) 
        prob = prob * 100
        self.occupancyGrid.data = prob.astype(int).flatten().tolist()
        self.occupancyMap.publish(self.occupancyGrid)

        
if __name__ == '__main__':
    rospy.init_node('occupancy_map')
    rate = rospy.Rate(2)
    # get parameters from launch file
    knownPose = rospy.get_param('knownPose', "True")
    knownPose = True if knownPose == "True" else False
    rospy.loginfo('Using mapping with known Poses: {}'.format(knownPose))
    occupancyMap = OccupancyMap(knownPose)
    while not rospy.is_shutdown():
        occupancyMap.reflection_model()
        rate.sleep()
    rospy.spin()


# TODO: we should subtract the origin of the robot in each step we divide by resolution
