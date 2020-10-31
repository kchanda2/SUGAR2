#!/usr/bin/env python

import roslib
import rospy
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from random import sample
from math import pow, sqrt
import urllib2
import time
import threading


current_room = "r1_m11"
constraints = []
task_status = [0,0]
previous_constraints = []
move = None
stop = False

class NavTest():
    def __init__(self):
        self.stateString = ""
        rospy.init_node('nav_test', anonymous=True)
        self.t1 = threading.Thread(target=self.check_constraints)
        self.t1.start()
        rospy.on_shutdown(self.shutdown)

        # How long in seconds should the robot pause at each location?
        # Goal state return values
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED',
                       'SUCCEEDED', 'ABORTED', 'REJECTED',
                       'PREEMPTING', 'RECALLING', 'RECALLED',
                       'LOST']

        # Set up the goal locations. Poses are defined in the map frame.
        # An easy way to find the pose coordinates is to point-and-click
        # Nav Goals in RViz when running in the simulator.
        # Pose coordinates are then displayed in the terminal
        # that was used to launch RViz.
        locations = dict()

        locations['hall_foyer'] = Pose(Point(0.643, 4.720, 0.000), Quaternion(0.000, 0.000, 0.223, 0.975))
        locations['hall_kitchen'] = Pose(Point(-1.994, 4.382, 0.000), Quaternion(0.000, 0.000, -0.670, 0.743))
        locations['hall_bedroom'] = Pose(Point(-3.719, 4.401, 0.000), Quaternion(0.000, 0.000, 0.733, 0.680))
        locations['living_room_1'] = Pose(Point(0.720, 2.229, 0.000), Quaternion(0.000, 0.000, 0.786, 0.618))
        locations['living_room_2'] = Pose(Point(1.471, 1.007, 0.000), Quaternion(0.000, 0.000, 0.480, 0.877))
        locations['dining_room_1'] = Pose(Point(-0.861, -0.019, 0.000), Quaternion(0.000, 0.000, 0.892, -0.451))

        # Publisher to manually control the robot (e.g. to stop it)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        rospy.loginfo("Waiting for move_base action server...")

        # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(60))

        rospy.loginfo("Connected to move base server")

        # A variable to hold the initial pose of the robot to be set by
        # the user in RViz
        initial_pose = PoseWithCovarianceStamped()

        # Variables to keep track of success rate, running time,
        # and distance traveled
        n_goals = 0
        n_successes = 0
        distance_traveled = 0
        start_time = rospy.Time.now()
        running_time = 0
        location = ""
        last_location = ""

        # Get the initial pose from the user
        rospy.loginfo("*** Click the 2D Pose Estimate button in RViz to set the robot's initial pose...")
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
        self.last_location = Pose()
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)

        # Make sure we have the initial pose
        while initial_pose.header.stamp == "":
            rospy.sleep(1)

        rospy.loginfo("Starting navigation test")

        # Begin the main loop and run through a sequence of locations
        while not rospy.is_shutdown() and self.stateString!="PREEMPTED" :
            #If we've gone through the current sequence,
            start with a new random sequence
            if i == n_locations:
                i = 0
                sequence = sample(locations, n_locations)
                # Skip over first location if it is the same as
                # the last location
                if sequence[0] == last_location:
                    i = 1
            
            # Get the next location in the current sequence
            location = sequence[i]
            
            # Keep track of the distance traveled.
            # Use updated initial pose if available.
            if initial_pose.header.stamp == "":
                distance = sqrt(pow(locations[location].position.x -
                                    locations[last_location].position.x, 2) +
                                pow(locations[location].position.y -
                                    locations[last_location].position.y, 2))
            else:
                rospy.loginfo("Updating current pose.")
                distance = sqrt(pow(locations[location].position.x -
                                    initial_pose.pose.pose.position.x, 2) +
                                pow(locations[location].position.y -
                                    initial_pose.pose.pose.position.y, 2))
                initial_pose.header.stamp = ""
            
            # Store the last location for distance calculations
            last_location = location
            
            # Increment the counters
            i += 1
            n_goals += 1
            #
            # # Set up the next goal location
            self.goal = MoveBaseGoal()
            self.goal.target_pose.pose.position =  Point(-2.11112529147,2.62306873765,0)
            self.goal.target_pose.pose.orientation.x = 0.0
            self.goal.target_pose.pose.orientation.y = 0.0
            self.goal.target_pose.pose.orientation.z = 0.85067259968
            self.goal.target_pose.pose.orientation.w = 0.525695851376
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()

            # Let the user know where the robot is going next
            rospy.loginfo("Going to: Destination")

            # Start the robot toward the next location
            self.move_base.send_goal(self.goal)

            # Allow 5 minutes to get there
            finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))

            # Check for success or failure
            if not finished_within_time:
                self.move_base.cancel_goal()
                rospy.loginfo("Timed out achieving goal")
            else:
                state = self.move_base.get_state()
                self.stateString = str(goal_states[state])
                if state == GoalStatus.SUCCEEDED:
                    rospy.loginfo("Goal succeeded!")
                    rospy.loginfo("State:" + str(state))
                else:
                  rospy.loginfo("Goal failed with error code: " + str(goal_states[state]))


    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose

    def get_constraints(self):
        global constraints
        global previous_constraints
        data = urllib2.urlopen("http://perceptobot.com/ar_demo/constraint.txt") # read only 20 000 chars
        previous_constraints = constraints
        constraints = []
        for line in data:
            constraints.append(line)

    def check_constraints(self):
        print "I am checking constraints"
        while(1):
            self.get_constraints()
            if(previous_constraints!=constraints):
                print "Need Generating new plan due to addition of constraint."
                self.shutdown()

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.move_base.cancel_all_goals()
        rospy.sleep(2)
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)

def trunc(f, n):
    # Truncates/pads a float f to n decimal places without rounding
    slen = len('%.*f' % (n, f))
    return float(str(f)[:slen])

if __name__ == '__main__':
    try:
        NavTest()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("AMCL navigation test finished.")
