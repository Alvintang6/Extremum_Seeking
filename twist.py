#!/usr/bin/env python

import roslib
import rospy
import std_msgs.msg
from geometry_msgs.msg import Twist
import message_filters
from line_laser_ros.msg import CleanData

def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)

class MobileTwist:
    
    speed = 1
    turn = 1.0
    twist = Twist()
    k = 0.0002
    delta_R = 0
    def __init__(self):   # _init_ method defines the instantiation operation."self" variablerepresents the instance of the object itself
        self.pub_twist = rospy.Publisher('cmd_vel',Twist,queue_size=1)
        self.subscriber_data = rospy.Subscriber("cleandata", CleanData, self.callback1,queue_size=1)
        self.subscriber_pred = rospy.Subscriber("pred",std_msgs.msg.Int16, self.callback2, queue_size=1)
        self.subscriber_count = rospy.Subscriber("count",std_msgs.msg.Int32,self.callback3,queue_size=1)

    def callback3(self,count):
        self.count = count

    def callback1(self,cleandata):
        self.intensity = cleandata.intensity
        self.range = cleandata.range

    def diffcal2(self):
        if self.pred==0:
            self.delta_R = -(776.66*(805/self.range**1.61-37))/self.range**2.61-0.0332
            return self.delta_R
        elif self.pred == 1:
            self.delta_R = -(389.53*(511.2/self.range**1.27-110.9))/self.range**2.27-0.032
            return self.delta_R
        elif self.pred == 2:
            if self.range <=2.7:
                self.delta_R = - (226.18*(658.0/self.range**0.57 - 442.74))/self.range**1.57 - 0.0332
                return self.delta_R
            else:# self.range > 2.7:
                self.delta_R = 38.26*self.range - (226.18*(658.0/self.range**0.57 - 442.74))/self.range**1.57 - 96.3165
                return self.delta_R
        elif self.pred == 3:
            if self.range <= 2:
                self.delta_R = - (281.97*(448.0/self.range**1.049 - 281.2))/self.range**2.049 - 0.0332
                return self.delta_R
            else:# self.range >2:
                self.delta_R = 33.68*self.range - (281.9712*(448.0/self.range**1.049 - 281.2))/self.range**2.049 - 51.79
                return self.delta_R

    def callback2(self,pred):
        self.pred = pred.data
        r = rospy.Rate(10)
        #while self.pred is not None
        if self.range > 4.5:
            x = 0.2
                
        else:
            self.diffcal2()
            if abs(self.delta_R)<1000:
                x = self.delta_R*self.k
            else: 
                x = 0.3*self.delta_R/abs(self.delta_R)
                
        self.twist.linear.x = x*self.speed; self.twist.linear.y = -0.15; self.twist.linear.z = 0
        self.twist.angular.x = 0; self.twist.angular.y = 0; self.twist.angular.z = 0

        self.pub_twist.publish(self.twist)
        r.sleep()
        
if __name__=="__main__": 
    rospy.init_node('twist')
    #r = rospy.Rate(10)
    mobiletwist = MobileTwist()
    try:
        #r.sleep()
        rospy.spin()
    except:
        print("sth wrong")
