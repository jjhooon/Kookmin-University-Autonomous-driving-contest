#!/usr/bin/python

import rospy, math
from rospy import Subscriber
from std_msgs.msg import Int32MultiArray

a = []
b = []
def callback(msg):
    print(msg.data)
    a.append(msg.data[2])
    b.append(msg.data[1]) #start 569

rospy.init_node('guide')
motor_pub = rospy.Publisher('xycar_motor_msg', Int32MultiArray, queue_size=1)
ultra_sub = rospy.Subscriber('ultrasonic', Int32MultiArray,callback)

xycar_msg = Int32MultiArray()

while not rospy.is_shutdown():
    for i in range(0, len(a), 1):
        if len(a) == 1:
            angle = 0
            xycar_msg.data = [angle, 25]
            motor_pub.publish(xycar_msg)
        else:
            if a[0] == a[-1]:
                angle = 0
                xycar_msg.data = [angle, 25]
                motor_pub.publish(xycar_msg)
            else:
                if b[-1] <= 550:
                    if a[0] + 30 <= a[-1]:
                        angle = 90
                        xycar_msg.data = [angle, 15]
                        motor_pub.publish(xycar_msg)
                    else:
                        angle = -30
                        xycar_msg.data = [angle,20]
                        motor_pub.publish(xycar_msg)
                else:
                    angle = 0
                    xycar_msg.data = [angle, 10]
                    motor_pub.publish(xycar_msg)