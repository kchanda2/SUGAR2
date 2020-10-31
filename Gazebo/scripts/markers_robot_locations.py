#!/usr/bin/python
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import rospy
import math
import urllib2
import threading
import time
import random
from geometry_msgs.msg import Point
import requests

stop_threads = False
green_robot_marker_id = 5111
red_robot_marker_id = 5112
blue_robot_marker_id = 5113

red_robot_current_location = [0,0]
blue_robot_current_location = [0,0]
green_robot_current_location = [0,0]

topic = 'visualization_marker_array'
count = 0
MARKERS_MAX = 1
markerArray = MarkerArray()
robot_marker_array = MarkerArray()
green_robot_path = 0.0
blue_robot_path = 0.0
red_robot_path = 0.0

def test_marker():
    global count
    global MARKERS_MAX
    global markerArray
    if(count>3):
        count=0
        markerArray = MarkerArray()
    for i in range(3):
        marker = Marker()
        marker.header.frame_id = "/map"
        marker.type = marker.CUBE
        marker.action = marker.ADD
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2
        marker.color.a = count*0.5
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = count + 1
        marker.pose.position.y = -0.461
        marker.pose.position.z = 0
        marker.id = count
        markerArray.markers.append(marker)
        count += 1
        print count
    publisher.publish(markerArray)
    rospy.sleep(0.01)
    return

def get_robots_current_location():
    while True:
        if stop_threads:
            break
        global red_robot_current_location,green_robot_current_location,blue_robot_current_location
        current_location = []
        target_url = "http://makeandroidapp.com/ar_demo/queue_manager/current_position_red_robot.txt"
        data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
        for line in data:
            red_robot_current_location = line.split(",")
        target_url = "http://makeandroidapp.com/ar_demo/queue_manager/current_position_blue_robot.txt"
        data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
        for line in data:
            blue_robot_current_location = line.split(",")
        target_url = "http://makeandroidapp.com/ar_demo/queue_manager/current_position_green_robot.txt"
        data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
        for line in data:
            green_robot_current_location = line.split(",")
        move_robot_new_location("blue")
        move_robot_new_location("green")
        move_robot_new_location("red")
        time.sleep(5)
    # for line in data: # files are iterable
    #     co_ordinates = []
    #     co_ordinates = line.split("  ")
    #     # print co_ordinates[0]
    #     # print co_ordinates[1]
    #     co_ordinates[1] = co_ordinates[1].strip()
    #     current_plan.append(co_ordinates)
    #
    # draw_plan(current_plan,"red")



def get_green_robot_plan():
    global green_robot_path
    current_plan = []
    try:
        response = requests.get('http://perceptobot.com/ar_demo/entire_plan_robot_green.txt')
        retrieved_text = response.text
        obtained_plan = retrieved_text.split("\n")
        for line in obtained_plan:
            if not line.strip():
                continue
            co_ordinates = []
            co_ordinates = line.split("  ")
            co_ordinates[1] = co_ordinates[1].strip()
            co_ordinates[0] = float(co_ordinates[0])
            co_ordinates[1] = float(co_ordinates[1])
            current_plan.append(co_ordinates)
        green_robot_path = current_plan[:]
        print "------------------------Green-------------------------------"
        print green_robot_path
        print "------------------------Green Over-------------------------------"
    except Exception as e:
        print e
            # print('Error in get_green_robot_plan')

    draw_plan(green_robot_path,"green")
    return
    # print current_plan



def get_red_robot_plan():
    global green_robot_path
    current_plan = []
    try:
        response = requests.get('http://perceptobot.com/ar_demo/entire_plan_robot_red.txt')
        retrieved_text = response.text
        obtained_plan = retrieved_text.split("\n")
        for line in obtained_plan:
            if not line.strip():
                continue
            co_ordinates = []
            co_ordinates = line.split("  ")
            co_ordinates[1] = co_ordinates[1].strip()
            co_ordinates[0] = float(co_ordinates[0])
            co_ordinates[1] = float(co_ordinates[1])
            current_plan.append(co_ordinates)
        red_robot_path = current_plan[:]
    except Exception as e:
        print e
            # print('Error in get_green_robot_plan')

    draw_plan(red_robot_path,"red")
    return
    # print current_plan

def get_blue_robot_plan():
    global green_robot_path
    current_plan = []
    try:
        response = requests.get('http://perceptobot.com/ar_demo/entire_plan_robot_blue.txt')
        retrieved_text = response.text
        obtained_plan = retrieved_text.split("\n")
        for line in obtained_plan:
            if not line.strip():
                continue
            co_ordinates = []
            co_ordinates = line.split("  ")
            co_ordinates[1] = co_ordinates[1].strip()
            co_ordinates[0] = float(co_ordinates[0])
            co_ordinates[1] = float(co_ordinates[1])
            current_plan.append(co_ordinates)
        blue_robot_path = current_plan[:]
    except Exception as e:
        print e
            # print('Error in get_green_robot_plan')

    draw_plan(blue_robot_path,"blue")
    return
    # print current_plan

def get_blue_robot_plan():
    global red_robot_path
    current_plan = []
    target_url = "http://perceptobot.com/ar_demo/entire_plan_robot_red.txt"
    data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
    for line in data: # files are iterable
        co_ordinates = []
        co_ordinates = line.split("  ")
        # print co_ordinates[0]
        # print co_ordinates[1]
        co_ordinates[1] = co_ordinates[1].strip()
        current_plan.append(co_ordinates)
    red_robot_path = current_plan[:]
    print "------------------------Red-------------------------------"
    print red_robot_path
    print "------------------------Red Over-------------------------------"
    # draw_plan(red_robot_path,"red")

def get_blue_robot_plan():
    print "entering to get blue robot plan"
    global blue_robot_path
    current_plan = []
    target_url = "http://perceptobot.com/ar_demo/entire_plan_robot_blue.txt"
    data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
    for line in data: # files are iterable
        co_ordinates = []
        co_ordinates = line.split("  ")
        # print co_ordinates[0]
        # print co_ordinates[1]
        co_ordinates[1] = co_ordinates[1].strip()
        current_plan.append(co_ordinates)
    blue_robot_path = current_plan[:]
    print "------------------------Blue-------------------------------"
    print blue_robot_path
    print "------------------------Blue Over-------------------------------"
    # draw_plan(blue_robot_path,"blue")

def draw_plan(plan_array,color_of_robot):
    i=0
    global count
    for current_plan_point in plan_array:
        current_marker_point = Point(current_plan_point[0],current_plan_point[1],0)
        marker = Marker()
        if(color_of_robot == "green"):
            marker.color.r = 0.0
            marker.color.g = 1.0
            marker.color.b = 0.0
        elif(color_of_robot == "blue"):
            marker.color.r = 0.0
            marker.color.g = 0.0
            marker.color.b = 1.0
        elif(color_of_robot == "red"):
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0

        marker.header.frame_id = "/map"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = 0.3
        marker.scale.y  = 0.3
        marker.scale.z = 0.3
        marker.color.a = 1.0
        # marker.color.r = 1.0
        # marker.color.g = 0.0
        # marker.color.b = 0.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = float(current_marker_point.x)
        marker.pose.position.y = float(current_marker_point.y)
        marker.pose.position.z = float(current_marker_point.z)
        marker.id = count
        markerArray.markers.append(marker)
        i+=1
        count+=1

    publisher.publish(markerArray)
    rospy.sleep(1)



def move_robot(path,color_of_robot):
    for current_coordinates in path:
        marker_id = 0
        current_robot_loc = Point(current_coordinates[0],current_coordinates[1],0)
        print current_coordinates[0]
        robot_marker = Marker()
        if(color_of_robot == "green"):
            marker_id = count+2
            robot_marker.color.r = 0.0
            robot_marker.color.g = 1.0
            robot_marker.color.b = 0.0
        elif(color_of_robot == "blue"):
            marker_id = count+1
            robot_marker.color.r = 0.0
            robot_marker.color.g = 0.0
            robot_marker.color.b = 1.0
        elif(color_of_robot == "red"):
            marker_id = count+3
            robot_marker.color.r = 1.0
            robot_marker.color.g = 0.0
            robot_marker.color.b = 0.0

        robot_marker.header.frame_id = "/map"
        robot_marker.type = robot_marker.CUBE
        robot_marker.action = robot_marker.ADD
        robot_marker.scale.x = 0.5
        robot_marker.scale.y  = 0.5
        robot_marker.scale.z = 0.5
        robot_marker.color.a = 1.0
        # marker.color.r = 1.0
        # marker.color.g = 0.0
        # marker.color.b = 0.0
        robot_marker.pose.orientation.w = 1.0
        robot_marker.pose.position.x = float(current_robot_loc.x)
        robot_marker.pose.position.y = float(current_robot_loc.y)
        robot_marker.pose.position.z = float(current_robot_loc.z)
        robot_marker.id = marker_id
        robot_marker_array.markers.append(robot_marker)
        publisher.publish(robot_marker_array)
        rospy.sleep(random.randint(10,50)*0.1)

def move_robot_new_location(color_of_robot):
    marker_id = 0
    current_robot_loc = Point(0,0,0)
    # print current_coordinates[0]
    robot_marker = Marker()
    if(color_of_robot == "green"):
        marker_id = green_robot_marker_id
        robot_marker.color.r = 0.0
        robot_marker.color.g = 1.0
        robot_marker.color.b = 0.0
        current_robot_loc.x = green_robot_current_location[0]
        current_robot_loc.y = green_robot_current_location[1]
    elif(color_of_robot == "blue"):
        marker_id = blue_robot_marker_id
        robot_marker.color.r = 0.0
        robot_marker.color.g = 0.0
        robot_marker.color.b = 1.0
        current_robot_loc.x = blue_robot_current_location[0]
        current_robot_loc.y = blue_robot_current_location[1]
    elif(color_of_robot == "red"):
        marker_id = red_robot_marker_id
        robot_marker.color.r = 1.0
        robot_marker.color.g = 0.0
        robot_marker.color.b = 0.0
        current_robot_loc.x = red_robot_current_location[0]
        current_robot_loc.y = red_robot_current_location[1]

    robot_marker.header.frame_id = "/map"
    # robot_marker.type = robot_marker.MESH_RESOURCE;
    # robot_marker.mesh_resource = "package://asp_navigation/meshes/Turtlebot2i.stl";
    robot_marker.type = robot_marker.CUBE
    robot_marker.action = robot_marker.ADD
    robot_marker.scale.x = 1
    robot_marker.scale.y  = 1
    robot_marker.scale.z = 1
    robot_marker.color.a = 1.0
    # marker.color.r = 1.0
    # marker.color.g = 0.0
    # marker.color.b = 0.0
    robot_marker.pose.orientation.w = 1.0
    robot_marker.pose.position.x = float(current_robot_loc.x)
    robot_marker.pose.position.y = float(current_robot_loc.y)
    robot_marker.pose.position.z = float(current_robot_loc.z)
    robot_marker.id = marker_id
    robot_marker_array.markers.append(robot_marker)
    publisher.publish(robot_marker_array)
    rospy.sleep(0.5)

def get_all_robot_plans():
    global count
    while True:

        print "COde 5"
        delete_all()
        count = 0
        #delete_markers here for robot previous plans
        get_blue_robot_plan()
        get_red_robot_plan()
        get_green_robot_plan()
        time.sleep(15)

def move_all_robots():
    robot_locations_thread = threading.Thread(target=get_robots_current_location)
    t1 = threading.Thread(target=get_all_robot_plans)
    # t3 = threading.Thread(target=move_robot,args=(red_robot_path,"red"))
    robot_locations_thread.start()
    t1.start()
    robot_locations_thread.join()
    t1.join()

def delete_all():
    print "Deleting markers"
    for i in range(1000):
        marker = Marker()
        marker.header.frame_id = "/map"
        marker.type = marker.SPHERE
        marker.action = marker.DELETE
        markerArray.markers.append(marker)
        marker.id = i
    publisher.publish(markerArray)
    rospy.sleep(0.01)


if __name__ == '__main__':
    global stop_threads
    try:
        rospy.init_node('test_marker')
        publisher = rospy.Publisher(topic, MarkerArray)
        move_all_robots()
    txt = raw_input("What to do now: ")
    if(int(txt) == 1):
        test_marker()
    elif(int(txt) == 2):
        delete_all()
    elif(int(txt) == 3):
        get_green_robot_plan()
        get_red_robot_plan()
        get_blue_robot_plan()
        move_all_robots()

    except rospy.ROSInterruptException:
            stop_threads = True
            print "finished!"
    # marker = Marker()
    # marker.header.frame_id = "/map"
    # marker.type = marker.CUBE
    # marker.action = marker.ADD
    # marker.scale.x = 0.2
    # marker.scale.y = 0.2
    # marker.scale.z = 0.2
    # marker.color.a = 1.0
    # marker.color.r = 1.0
    # marker.color.g = 1.0
    # marker.color.b = 0.0
    # marker.pose.orientation.w = 1.0
    # marker.pose.position.x = math.cos(count / 50.0)
    # marker.pose.position.y = math.cos(count / 40.0)
    # marker.pose.position.z = math.cos(count / 30.0)
    # # We add the new marker to the MarkerArray, removing the oldest
    # # marker from it when necessary
    # if(count > MARKERS_MAX):
    #    markerArray.markers.pop(0)
    #
    # markerArray.markers.append(marker)
    #
    # # Renumber the marker IDs
    # id = 0
    # for m in markerArray.markers:
    #    m.id = id
    #    id += 1
    #
    # # Publish the MarkerArray
    # publisher.publish(markerArray)
    #
    # count += 1
    #
    # rospy.sleep(0.01)
