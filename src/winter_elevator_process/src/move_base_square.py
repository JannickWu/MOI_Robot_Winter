#!/usr/bin/env python

""" move_base_square.py - Version 1.1 2013-12-20

    Command a robot to move in a square using move_base actions..

    Created for the Pi Robot Project: http://www.pirobot.org
    Copyright (c) 2012 Patrick Goebel.  All rights reserved.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.5
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:
    
    http://www.gnu.org/licenses/gpl.htmlPoint
      
"""

import rospy
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from visualization_msgs.msg import Marker
from math import radians, pi
import time

class MoveBaseFloor():
    def __init__(self):
        rospy.init_node('nav_test', anonymous=False)
        
        rospy.on_shutdown(self.shutdown)       
        '''
        # Create a list to hold the target quaternions (orientations)
        quaternions = list()
        
        # Then convert the angles to quaternions
        q_angle = quaternion_from_euler(0, 0, angle, axes='sxyz')
        q = Quaternion(*q_angle)
        quaternions.append(q)
        
        # Create a list to hold the waypoint poses
        waypoints = list()
        
        # Append each of the four waypoints to the list.  Each waypoint
        # is a pose consisting of a position and orientation in the map frame.
        waypoints.append(Pose(Point(square_size, 0.0, 0.0), quaternions[0]))
        waypoints.append(Pose(Point(square_size, square_size, 0.0), quaternions[1]))
        waypoints.append(Pose(Point(0.0, square_size, 0.0), quaternions[2]))
        waypoints.append(Pose(Point(0.0, 0.0, 0.0), quaternions[3]))
        
        # Initialize the visualization markers for RViz
        self.init_markers()
        
        # Set a visualization marker at each waypoint        
        for waypoint in waypoints:           
            p = Point()
            p = waypoint.position
            self.markers.points.append(p)
        '''    
        # Publisher to manually control the robot (e.g. to stop it, queue_size=5)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
        
        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        
        rospy.loginfo("Waiting for move_base action server...")
        
        # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(180))
        
        rospy.loginfo("Connected to move base server")
        rospy.loginfo("Starting navigation test")
        
        # Initialize a counter to track waypoints
        i = 0
        # Intialize the waypoint goal
        
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x=5.53
        goal.target_pose.pose.position.y=-1.45
        goal.target_pose.pose.position.z=0.0
        #angle 0.604
        goal.target_pose.pose.orientation.x=0.0
        goal.target_pose.pose.orientation.y=0.0
        goal.target_pose.pose.orientation.z=-0.654
        goal.target_pose.pose.orientation.w=0.757
        self.move(goal)
        time.sleep(5)
        
        goal2 = MoveBaseGoal()
        goal2.target_pose.header.frame_id = 'map'
        goal2.target_pose.header.stamp = rospy.Time.now()
        goal2.target_pose.pose.position.x=5.53
        goal2.target_pose.pose.position.y=0.65
        goal2.target_pose.pose.position.z=0.0
        #angle 0.604
        goal2.target_pose.pose.orientation.x=0.0
        goal2.target_pose.pose.orientation.y=0.0
        goal2.target_pose.pose.orientation.z=0.71
        goal2.target_pose.pose.orientation.w=0.704
        self.move(goal2)
        
    def move(self, goal):
            # Send the goal pose to the MoveBaseAction server
            self.move_base.send_goal(goal)
            
            # Allow 20 minute to get there
            finished_within_time = self.move_base.wait_for_result(rospy.Duration(20*60)) 
            
            # If we don't get there in time, abort the goal
            if not finished_within_time:
                self.move_base.cancel_goal()
                rospy.loginfo("Timed out achieving goal")
            else:
                # We made it!
                state = self.move_base.get_state()
                if state == GoalStatus.SUCCEEDED:
                    rospy.loginfo("Goal succeeded!")

    def shutdown(self):
        #rospy.loginfo("Stopping the robot...")
        # Cancel any active goals
        #self.move_base.cancel_goal()
        #rospy.sleep(2)
        # Stop the robot
        #self.cmd_vel_pub.publish(Twist())
        rospy.sleep(0.1)

if __name__ == '__main__':
    try:
        MoveBaseFloor()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
