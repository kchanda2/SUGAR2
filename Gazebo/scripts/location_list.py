#!/usr/bin/python
import subprocess
import re
import sys

locations = {
		"ta_1":{"d1_n09_1":["0.377783249618,7.92581800226,-0.384135527805,0.923276717067","n09","2.208109168,6.1860268899,-0.384135527805,0.923276717067"]},
		"n09" :	 {"d1_n09_1":["2.208109168,6.1860268899,0.89695345947,0.442124972767","ta_1","0.377783249618,7.92581800226,0.89695345947,0.442124972767"]},
		"exit_corr" :    {"d1_exit_corr":["6.00, 19.2,-0.937243748076, 0.348674858131","one_side"]},
		"ta_2" :    {"d1_ta_2":["9.13128555878,-3.85044084279,0.258269787112,0.966072832174","one_side"]},
		"madhu_corr" :    {"d1_madhu_corr":["-6.21783926123,14.6042770751,-0.997049781118,0.0767576313632","one_side"]}
		}

object_locations = {
		"s0" : ["16.8617402029,-1.7861,0.565104035575,0.825019","16.8617402029,-1.7861,0.565104035575,0.825019","16.8617402029,-1.7861,0.565104035575,0.825019"],
		"s1" : ["6.37607619493,22.2553998406,-0.0918760220674,0.995770453754","6.37607619493,22.2553998406,-0.0918760220674,0.995770453754","6.37607619493,22.2553998406,-0.0918760220674,0.995770453754"],
		"s2" : ["-17.0002670876,13.8604234844,0.963803234841,0.266614561699","-17.0002670876,13.8604234844,0.963803234841,0.266614561699","-17.0002670876,13.8604234844,0.963803234841,0.266614561699"],
		"drop_station" : "4.13,33.8,0.920566656085,0.390585498584"
		}

def find_location(goal):
	return locations[goal]

def find_object_loacation(object_name):
	return object_locations[object_name]

def find_door(door_name):
	print "Finding this door "+ door_name
	for location in sorted(locations.keys(), reverse=True):
		print location
		door_list = {}
		if(door_name in locations[location]):
			door_list = locations[location]
			door_list["room_name"] = location
			return locations[location]

def find_door_outside_room(door_name):
	print "Finding this door "+ door_name
	for location in sorted(locations.keys(), reverse=True):
		print location
		door_list = {}
		if(door_name in locations[location]):
			door_list = locations[location]
			door_list["room_name"] = location
			return locations[location]
		door_list = {}
		if(door_name in locations[i]):
			door_list = locations[i]
			door_list["room_name"] = location
			return locations[location]
