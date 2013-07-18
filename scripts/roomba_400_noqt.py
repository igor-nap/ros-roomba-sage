#!/usr/bin/env python

# Import the ROS libraries, and load the manifest file which through <depend package=... /> will give us access to the project dependencies
import roslib; roslib.load_manifest('roomba_400')
import rospy

# Import the joystick message
from sensor_msgs.msg import Joy

# Import the cmd_vel type message
from geometry_msgs.msg import Twist

# Finally the GUI libraries
#from PySide import QtCore, QtGui

import math

# define the default mapping between joystick buttons and their corresponding actions
ButtonEmergency = 0
ButtonLand      = 1
ButtonTakeoff   = 2

# define the default mapping between joystick axes and their corresponding directions
AxisRoll        = 0
AxisPitch       = 1
AxisYaw         = 3
AxisZ           = 4

# define the default scaling to apply to the axis inputs. useful where an axis is inverted
ScaleRoll       = 1.0
ScalePitch      = 1.0
ScaleYaw        = 1.0
ScaleZ          = 1.0

MIN_SCALE = 0.2
GO_STRAIGHT = 99
ZERO_FLOAT_ERROR = 0.001

# handles the reception of joystick packets
def ReceiveJoystickMessage(data):
	if data.buttons[ButtonEmergency]==1:
		rospy.loginfo("Emergency Button Pressed")
		#controller.SendEmergency()
	elif data.buttons[ButtonLand]==1:
		rospy.loginfo("Land Button Pressed")
		#controller.SendLand()
	elif data.buttons[ButtonTakeoff]==1:
		rospy.loginfo("Takeoff Button Pressed")
		#controller.SendTakeoff()
	else:
		twist = Twist()
		fwd = data.axes[AxisZ]
		turn = data.axes[AxisYaw]

		if abs(fwd) < MIN_SCALE:
			fwd = 0.0
		if abs(turn) < MIN_SCALE:
			turn = 0.0
		
		if abs(turn) > ZERO_FLOAT_ERROR:
			absturn = 1.0-1.0/abs(turn)
			invturn = math.copysign(absturn,turn)
		else:
			invturn = GO_STRAIGHT;

		twist.linear.x = fwd*ScaleZ
		twist.angular.z = invturn*ScaleYaw
		#rospy.loginfo(twist.linear.x)
		#rospy.loginfo(twist.angular.z)
		pubcmdVel.publish(twist)
		#controller.SetCommand(data.axes[AxisRoll]/ScaleRoll,data.axes[AxisPitch]/ScalePitch,data.axes[AxisYaw]/ScaleYaw,data.axes[AxisZ]/ScaleZ)


# Setup the application
if __name__=='__main__':
	import sys
	# Firstly we setup a ros node, so that we can communicate with the other packages
	rospy.init_node('roomba_400_joy')

	# Next load in the parameters from the launch-file
	ButtonEmergency = int (   rospy.get_param("~ButtonEmergency",ButtonEmergency) )
	ButtonLand      = int (   rospy.get_param("~ButtonLand",ButtonLand) )
	ButtonTakeoff   = int (   rospy.get_param("~ButtonTakeoff",ButtonTakeoff) )
	AxisRoll        = int (   rospy.get_param("~AxisRoll",AxisRoll) )
	AxisPitch       = int (   rospy.get_param("~AxisPitch",AxisPitch) )
	AxisYaw         = int (   rospy.get_param("~AxisYaw",AxisYaw) )
	AxisZ           = int (   rospy.get_param("~AxisZ",AxisZ) )
	ScaleRoll       = float ( rospy.get_param("~ScaleRoll",ScaleRoll) )
	ScalePitch      = float ( rospy.get_param("~ScalePitch",ScalePitch) )
	ScaleYaw        = float ( rospy.get_param("~ScaleYaw",ScaleYaw) )
	ScaleZ          = float ( rospy.get_param("~ScaleZ",ScaleZ) )

	# Now we construct our Qt Application and associated controllers and windows
	rospy.myargv(argv=sys.argv)
	#app = QtGui.QApplication(sys.argv)
	#display = DroneVideoDisplay()
	#controller = BasicDroneController()

	# subscribe to the /joy topic and handle messages of type Joy with the function ReceiveJoystickMessage
	subJoystick = rospy.Subscriber('/joy', Joy, ReceiveJoystickMessage)
	pubcmdVel = rospy.Publisher('/cmd_vel', Twist)
	
	# executes the QT application
	#display.show()
	#status = app.exec_()
 
	rospy.spin()

	# and only progresses to here once the application has been shutdown
	rospy.signal_shutdown('Great Driving!')
	sys.exit(status)