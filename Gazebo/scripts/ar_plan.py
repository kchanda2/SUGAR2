#!/usr/bin/env python
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseFeedback
import actionlib
import ftplib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, PoseWithCovarianceStamped, Quaternion, PoseStamped
from nav_msgs.srv import GetPlan
from nav_msgs.msg import Odometry
import time

start_x = 0.0
start_y = 0.0


def callback_pose(data):
        global start_x
        global start_y
        start_x = data.pose.pose.position.x
        start_y = data.pose.pose.position.y
        with open('robot_location.txt', 'w') as f:
             f.write(str(start_x)+","+str(start_y))
             f.close()

def upload_to_server():
	# Can be used for a Xammp server to store the state of the robots.



# Adds the robots poses to a file which can be transmitted to a server
def add_poses_to_file(poses):
    initial_x_coordinate = -100.0;
    initial_y_coordinate = -100.0;
    with open('entire_plan_robot_1.txt', 'a+') as f:
        for index in range(1, len(poses)):
            x_coordinate = float("{0:.2f}".format(poses[index].pose.position.x));
            y_coordinate = float("{0:.2f}".format(poses[index].pose.position.y));
            if ((x_coordinate <= initial_x_coordinate - 0.6) or (x_coordinate >= initial_x_coordinate + 0.6) or (y_coordinate <= initial_y_coordinate - 0.6) or (y_coordinate >= initial_y_coordinate + 0.6)):
                f.write(str(x_coordinate)+"  "+str(y_coordinate)+"\n")
                initial_x_coordinate = x_coordinate;
                initial_y_coordinate = y_coordinate;
        f.close()
    with open('robot_location.txt', 'w') as f:
        f.write(str(poses[len(poses)-1].pose.position.x)+","+str(poses[len(poses)-1].pose.position.y))
        f.close()



    except rospy.ROSInterruptException:
       rospy.loginfo("Ctrl-C caught. Quitting")
