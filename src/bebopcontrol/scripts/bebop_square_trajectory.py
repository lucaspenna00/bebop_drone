import rospy
import time ## controlling the time 
from geometry_msgs.msg import Twist ## controlling the velocity
import os

velocity_message = Twist()

abs_position_x = 0.0
abs_position_y = 0.0
abs_position_z = 0.0

def set_x_relative_position(x):

	'''
	Input:
	(x,y,z) = vector of position

	Task:
	publish velocity messages during the time linked to position
	'''
	global abs_position_x
	global abs_position_y
	global abs_position_z
	global velocity_message

	time_duration = abs(float(x/4))

	print(time_duration)

	timeout = time.time() + time_duration # 0.5 minutes from now

	while True:

		if x > 0:

			#print(time.time())

			velocity_message.linear.x = 4.0
			velocity_message.linear.y = 0.0
			velocity_message.linear.z = 0.0
			velocity_position_pub.publish(velocity_message)

			rate.sleep()

			if time.time() > timeout:

				#print("[ bebop2 WARN] Position reached! x: %f y: %f z: %f" % abs_position_x, abs_position_y, abs_position_z)

				return

		if x < 0:

			velocity_message.linear.x = -4.0
			velocity_message.linear.y = 0.0
			velocity_message.linear.z = 0.0
			velocity_position_pub.publish(velocity_message)

			rate.sleep()

			if time.time() > timeout:

				#print("[ bebop2 WARN] Position reached! x: %f y: %f z: %f" % abs_position_x, abs_position_y, abs_position_z)

				abs_position_x = abs_position_x + x

				return

def set_y_relative_position(y):

	'''
	Input:
	(x,y,z) = vector of position

	Task:
	publish velocity messages during the time linked to position
	'''
	global abs_position_x
	global abs_position_y
	global abs_position_z
	global velocity_message

	time_duration = abs(float(y/4))

	print(time_duration)

	timeout = time.time() + time_duration # 0.5 minutes from now

	while True:

		if y > 0:

			#print(time.time())

			velocity_message.linear.x = 0.0
			velocity_message.linear.y = 4.0
			velocity_message.linear.z = 0.0
			velocity_position_pub.publish(velocity_message)

			rate.sleep()

			if time.time() > timeout:

				#print("[ bebop2 WARN] Position reached! x: %f y: %f z: %f" % abs_position_x, abs_position_y, abs_position_z)

				return

		if y < 0:

			velocity_message.linear.x = 0.0
			velocity_message.linear.y = -4.0
			velocity_message.linear.z = 0.0
			velocity_position_pub.publish(velocity_message)

			rate.sleep()

			if time.time() > timeout:

				#print("[ bebop2 WARN] Position reached! x: %f y: %f z: %f" % abs_position_x, abs_position_y, abs_position_z)

				abs_position_y = abs_position_y + y

				return

def set_z_relative_position(z):

	'''
	Input:
	(x,y,z) = vector of position

	Task:
	publish velocity messages during the time linked to position
	'''
	global abs_position_x
	global abs_position_y
	global abs_position_z
	global velocity_message

	time_duration = abs(float(z/4))

	print(time_duration)

	timeout = time.time() + time_duration # 0.5 minutes from now

	while True:

		if z > 0:

			#print(time.time())

			velocity_message.linear.x = 0.0
			velocity_message.linear.y = 0.0
			velocity_message.linear.z = 4.0
			velocity_position_pub.publish(velocity_message)

			rate.sleep()

			if time.time() > timeout:

				#print("[ bebop2 WARN] Position reached! x: %f y: %f z: %f" % abs_position_x, abs_position_y, abs_position_z)

				return

		if z < 0:

			velocity_message.linear.x = 0.0
			velocity_message.linear.y = 0.0
			velocity_message.linear.z = -4.0
			velocity_position_pub.publish(velocity_message)

			rate.sleep()

			if time.time() > timeout:

				#print("[ bebop2 WARN] Position reached! x: %f y: %f z: %f" % abs_position_x, abs_position_y, abs_position_z)

				abs_position_z = abs_position_z + z

				return

## --- NODE --- ##

print("Welcome to the first node to control Parrot Bebop2 Drone.")
print("Developed by Skyrats Intelligent Drones team of Poli-USP.")

rospy.init_node('Bebop_2_Position_Control')

rate = rospy.Rate(20) # publish at 20 [Hz]

velocity_position_pub = rospy.Publisher('/bebop/cmd_vel', Twist, queue_size=10)

os.system("./bebop_takeoff.sh")

time.sleep(5)

print("[ bebop2 WARN] Takeoff succesfully")

while not rospy.is_shutdown():

	key = int(input("[ Skyrats wants to know] One more iteration?"))

	if key == 0:

		os.system("./land.sh")

		print("[ bebop2 WARN] Land succesfully")

	if key == 1:

		set_x_relative_position(5.0)
		print(abs_position_x, abs_position_y)
		time.sleep(2)

		set_y_relative_position(5.0)
		print(abs_position_x, abs_position_y)
		time.sleep(2)

		set_x_relative_position(-5.0)
		print(abs_position_x, abs_position_y)
		time.sleep(2)
		
		set_y_relative_position(-5.0)
		print(abs_position_x, abs_position_y)
		time.sleep(2)
