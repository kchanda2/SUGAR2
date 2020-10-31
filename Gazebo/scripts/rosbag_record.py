#!/usr/bin/env python

import rospy
import rosbag
import time
from sensor_msgs.msg import CompressedImage

bag = rosbag.Bag('camera.bag', 'w')

def callback(data):
	rospy.loginfo('writing to camera-bag!')
	bag.write('/camera/rgb/image_raw/compressed', data)
	time.sleep(.1)

def main():
	rospy.init_node("rosbag_record")
	rospy.Subscriber("/camera/rgb/image_raw/compressed", CompressedImage, callback)
	rospy.spin()

if __name__ == "__main__":
	try:
		main()
	finally:
		bag.close()
