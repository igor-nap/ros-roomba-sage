#!/usr/bin/env python

# Import the ROS libraries, and load the manifest file which through <depend package=... /> will give us access to the project dependencies
import roslib; roslib.load_manifest('roomba_400')
import rospy

from std_msgs.msg import Empty       	 # for land/takeoff/emergency

