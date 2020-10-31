#!/usr/bin/env python
import rospy
import actionlib
import asp_planning
import location_list
import Tkinter
import tkMessageBox
import ar_plan
import datetime
from ftplib import FTP
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseFeedback
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, PoseWithCovarianceStamped, Quaternion, PoseStamped
from nav_msgs.srv import GetPlan
from nav_msgs.msg import Odometry
from sound_play.libsoundplay import SoundClient
from actionlib_msgs.msg import *
import urllib2
import urllib
import std_srvs.srv
from std_msgs.msg import String, Float32, Empty
import time
import threading
import subprocess
import re
import sys
import copy
import requests

token_no = 3
robot_no = 1
completed = False

def get_token_for_going_in():
    global token_no
    response = requests.post('http://makeandroidapp.com/ar_demo/queue_manager/token_manager.php', data={'robot':robot_no})
    print "Response is :"+response.text

def get_token_for_going_out():
    global token_no
    response = requests.post('http://makeandroidapp.com/ar_demo/queue_manager/token_manager.php', data={'robot':robot_no,'action':'out'})
    token_no = int(response.text)
    print "token_no for going in is :"+str(token_no)

def wait_for_gothrough_turn():
    response = requests.get('http://makeandroidapp.com/ar_demo/queue_manager/token_manager_2.php', params={'token':token_no})
    my_turn = int(response.text)
    if int(my_turn) == 1:
        return True
    else:
        return False

def wait_for_gothrough_turn_out():
    response = requests.get('http://makeandroidapp.com/ar_demo/queue_manager/token_manager_2.php', params={'token':token_no,'action':'going_out'})
    my_turn = int(response.text)
    if int(my_turn) == 1:
        return True
    else:
        return False

def wait_for_door_open():
    response = requests.get('http://makeandroidapp.com/ar_demo/queue_manager/token_manager.php', params={'door_action':'going_in'})
    my_turn = int(response.text)
    if int(my_turn) == 1:
        return True
    else:
        return False

def increment_ticket(action):
    global token_no
    response = requests.post('http://makeandroidapp.com/ar_demo/queue_manager/token_manager_2.php', data={'increment_ticket':action})
    print "Next robot to go through door is"+response.text

def increment_ticket(action):
    global token_no
    response = requests.post('http://makeandroidapp.com/ar_demo/queue_manager/token_manager_2.php', data={'increment_ticket':action})
    print "Next robot to go through door is"+response.text

def callback_pose(data):
        start_x = data.pose.pose.position.x
        start_y = data.pose.pose.position.y
        print "Uploading now"
        response = requests.post('http://makeandroidapp.com/ar_demo/queue_manager/update_position_red_robot.php', data={'x':1.02,'y':2.04})
        print response.text

def update_values():
    response = requests.post('http://makeandroidapp.com/ar_demo/queue_manager/update_position_green_robot.php', data={'x':1.02,'y':2.04})
    print response.text

    # rospy.Subscriber ('/amcl_pose',PoseWithCovarianceStamped, callback_pose)
    # rospy.sleep(0.5)
    time.sleep(0.5)

def change_speed():
    pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
    msg = Twist()
    speed = 0.1
    msg.linear.x = speed
    pub.publish(msg)

def upload_to_server():
	# server = 'ftp.quickkaro.com'
	# username = 'final_try@perceptobot.com'
	# password = 'final_passwords'
	# ftp_connection = ftplib.FTP(server, username, password)
	# remote_path = "/"
	# ftp_connection.cwd(remote_path)
	# fh = open("object_s0.txt", 'rb')
	# ftp_connection.storbinary('STOR entire_plan_robot_blue.txt', fh)
	# fh.close()

    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect('ftp.quickkaro.com', 21)
    ftp.login('final_try@perceptobot.com','final_password')
    # ftp_upload()
    ftp.cwd("/")
    fp = open("object_s0.txt", 'rb')
    ftp.storbinary('STOR entire_plan_robot_blue.txt', fp, 1024)
    fp.close()
    print "after upload " + localfile + " to " + remotefile

def ftp_upload(localfile, remotefile):
    ftp.cwd("/")
    fp = open("object_s0.txt", 'rb')
    ftp.storbinary('STOR entire_plan_robot_blue.txt', fp, 1024)
    fp.close()
    print "after upload " + localfile + " to " + remotefile

def make_ar_plan():
    global start_x
    global start_y
    rospy.wait_for_service('/move_base/make_plan')
    make_plan = rospy.ServiceProxy('/move_base/make_plan', GetPlan)
    # with open('robot_location.txt','a+') as robot_loc:
    #     robot_loc.seek(0)
    #     current_robot_location = robot_loc.readline()
    #     robot_loc.close()
    #     current_robot_location_coordinates = current_robot_location.split(",")
    start_x = "1.96071595355"
    start_y = "6.33601683536"

    start = PoseStamped()
    goal = PoseStamped()
    start.header.frame_id = "map"
    goal.header.frame_id = "map"
    tolerance = 0.0
    start.pose.position.x= float(start_x)
    start.pose.position.y= float(start_y)
    goal.pose.position.x = float(-17.0002670876)
    goal.pose.position.y = float(13.8604234844)
    plan_response = make_plan(start = start, goal = goal, tolerance = tolerance)
    poses = plan_response.plan.poses
    add_poses_to_file(poses)
    upload_to_server()
    # print poses

def test_ar_planner(task_to_be_done):
    try:
        response = requests.get('http://perceptobot.com/ar_demo/update_plan.php', params={'robot_color':'blue','object_number':task_to_be_done})
    except:
        print('Error in update_loaded')

def add_poses_to_file(poses):
    initial_x_coordinate = -100.0;
    initial_y_coordinate = -100.0;
    with open('/home/phoenix/research_ws/src/asp_navigation/scripts/entire_plan_robot_1.txt', 'a+') as f:
        for index in range(1, len(poses)):
            x_coordinate = float("{0:.2f}".format(poses[index].pose.position.x));
            y_coordinate = float("{0:.2f}".format(poses[index].pose.position.y));

            if ((x_coordinate <= initial_x_coordinate - 0.6) or (x_coordinate >= initial_x_coordinate + 0.6) or (y_coordinate <= initial_y_coordinate - 0.6) or (y_coordinate >= initial_y_coordinate + 0.6)):
                f.write(str(x_coordinate)+"  "+str(y_coordinate)+"\n")
                initial_x_coordinate = x_coordinate;
                initial_y_coordinate = y_coordinate;
        f.close()

def checkdoor(current_location,goal_location):
    max_call = 0
    soundhandle = SoundClient()
    current_location_coordinates = current_location.split(",")
    goal_location_coordinates = goal_location.split(",")
    rospy.Subscriber ('/amcl_pose',PoseWithCovarianceStamped, callback_pose)
    rospy.wait_for_service('move_base/NavfnROS/make_plan')
    make_plan = rospy.ServiceProxy('move_base/NavfnROS/make_plan', GetPlan)
    start = PoseStamped()
    goal = PoseStamped()
    start.header.frame_id = "map"
    goal.header.frame_id = "map"
    tolerance = 0.0
    # print current_location
    start.pose.position.x= float(current_location_coordinates[0])
    start.pose.position.y= float(current_location_coordinates[1])
    goal.pose.position.x = float(goal_location_coordinates[0])
    goal.pose.position.y = float(goal_location_coordinates[1])
    plan_response = make_plan(start = start, goal = goal, tolerance = tolerance)
    poses = plan_response.plan.poses
    # print poses
    if(max_call>5):
        #rospy.ServiceProxy('/move_base/clear_costmaps',std_srvs.srv.Empty())
        clear_cost_map()
        max_call = 0
    if not poses:
    	if(max_call ==0):
            soundhandle.say('Please Open the door for me.')
            rospy.sleep(4)
        max_call = max_call+1
    	print "Please Open the door for me."
        print "I want to go to "+goal_location
        time.sleep(5)
        return False
    else:
        soundhandle.say('Thank you for opening the door.')
        rospy.sleep(3)
        print "Thank you."
        return True


if __name__ == '__main__':
    try:
        rospy.init_node('asp_navigator_py')
        door_list = location_list.find_door_edit("d1_n09_1")
        print door_list

    except rospy.ROSInterruptException:
            print "finished!"
