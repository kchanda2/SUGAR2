import datetime
import urllib2
import urllib
import time
import threading
import subprocess
import re
import sys

token_no = 1
robot_no = 1

def wait_for_gothrough_turn():
    data = urllib2.urlopen("http://perceptobot.com/ar_demo/queue_manager/token_manager.php?token="+str(token_no)) # read only 20 000 chars
    for line in data:
        my_turn = int(line)
    if int(my_turn) == 1:
        return True
    else:
        return False

def wait_for_gothrough_turn_out():
    data = urllib2.urlopen("http://perceptobot.com/ar_demo/queue_manager/token_manager.php?action=going_out&token="+str(token_no)) # read only 20 000 chars
    for line in data:
        my_turn = int(line)
    if int(my_turn) == 1:
        return True
    else:
        return False

def get_token_for_going_out():
    global token_no
    time.sleep(2)
    data = urllib2.urlopen("http://perceptobot.com/ar_demo/queue_manager/token_manager.php?action=going_out&robot="+str(robot_no))
    for line in data:
        token_no = int(line)
    print "token_no for going out is :"+str(token_no)

def get_token_for_going_in():
    global token_no
    time.sleep(2)
    data = urllib2.urlopen("http://perceptobot.com/ar_demo/queue_manager/token_manager.php?robot="+str(robot_no))
    for line in data:
        token_no = int(line)
    print "token_no for going in is :"+str(token_no)

def token_reset_final():
    time.sleep(3)
    query_args = {'reset_token_please':'yes'}
    data = urllib.urlencode(query_args)
    url = "http://perceptobot.com/ar_demo/queue_manager/token_manager.php?completed=yes"
    reset_token_value = 0
    request = urllib2.Request(url,data)
    response = urllib2.urlopen(request)
    html = response.read()
    print "Token reset after final drop?"+html
    global token_no

def increment_ticket(action):
    time.sleep(3)
    query_args = {'reset_token_please':'yes'}
    data = urllib.urlencode(query_args)
    url = "http://perceptobot.com/ar_demo/queue_manager/token_manager.php?increment_ticket="+str(action)
    reset_token_value = 0
    request = urllib2.Request(url,data)
    response = urllib2.urlopen(request)
    html = response.read()
    print "Next robot to go through door is"+html
    global token_no

def token_reset():
    global token_no
    token_no = -99
    time.sleep(3)
    reset_token_value =1
    query_args = {'reset_token_please':'yes'}
    data = urllib.urlencode(query_args)
    url = "http://perceptobot.com/ar_demo/queue_manager/token_manager.php?action=going_out&reset_token=1"
    reset_token_value = 0
    request = urllib2.Request(url,data)
    response = urllib2.urlopen(request)
    html = response.read()
    print "Token reset done?"+html
    global token_no

