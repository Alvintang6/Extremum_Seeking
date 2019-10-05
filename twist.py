#!/usr/bin/env python

import roslib
import rospy
import std_msgs.msg
from geometry_msgs.msg import Twist
import message_filters
from scipy import signal
from line_laser_ros.msg import CleanData

def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)

class MobileTwist:
    
    speed = 1
    turn = 1.0
    twist = Twist()
    k = 0.0002
    filterorder = 2
    delta_R = 0


    def __init__(self): # _init_ method defines the instantiation operation."self" variablerepresents the instance of the object itself
        self.flag_inital = 1
        self.HPFhis = np.zeros(filterorder + 1, dtype=float)
        self.Yout = np.zeros(filterorder + 1, dtype=float)
        self.b, self.a = signal.butter(filterorder, 0.09, 'highpass')
        self.last_pred = 0
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

    def timer_EI(self,pred):
        if self.pred == self.last_pred:
            self.timer = self.timer+1
        else:
            self.timer = 0
        self.last_pred = self.pred

    def Esc(self):
        for k in range(1, filterorder + 1):
            self.Yout[k - 1] = self.Yout[k]
            self.HPFhis[k - 1] = self.HPFhis[k]

        # should using Yout[fiterorder] = J(y_f,y_p,y_i) as input here
        Yout[filterorder] = xx[i]
        HPFnew = 0

        for j in range(1, filterorder + 2):
            HPFnew = HPFnew + self.b[j - 1] * self.Yout[filterorder + 1 - j]

        for j in range(2, filterorder + 2):
            HPFnew = HPFnew - self.a[j - 1] * self.HPFhis[filterorder + 1 - j]

        HPFhis[filterorder] = HPFnew
        # t_now may need to use the timer inside ros
        t_now = t_now + dt
        dr = HPFnew * math.sin(omega * t_now + phase)
        R = R + dr * dt * K
        Rd = R + math.sin(omega * t_now + phase)
        return Rd

    def direct_reset(self):
        if self.now_EI==0:
            self.delta_R = 1
            return self.delta_R
        elif self.now_EI == 1:
            self.delta_R = 2
            return self.delta_R
        elif self.now_EI == 2:
            if self.range <=2.7:
                self.delta_R = 3
                return self.delta_R
            else:# self.range > 2.7:
                self.delta_R = 4
                return self.delta_R
        elif self.now_EI == 3:
            if self.range <= 2:
                self.delta_R = 5
                return self.delta_R
            else:# self.range >2:
                self.delta_R = 6
                return self.delta_R

    def callback2(self,pred):
        MOVE = 1
        self.pred = pred.data
        r = rospy.Rate(10)
        timer_EI()
        #while self.pred is not None

        #(inital with the Ei dont change in 5 times) and (getting into new EI and Range_error > thershold)
        if (self.flag_inital == 0 and self.timer >=5) or (self.use_opt==1 and error_r > error_threshold):

            if (self.flag_inital == 0 and self.timer >=5):
                self.now_EI = pred.data
                self.flag_inital = 1
            Rd = direct_reset()

        elif  self.timer == 7 :
            self.use_opt = 1
            self.now_EI = pred.data
            Rd = direct_reset()

        elif self.flag_inital == 1 :
            Rd = Esc()
        # here else means flag_inital = 0  and  timer<= 5
        else:
            MOVE = 0

        if (error_r < error_threshould and self.use_opt == 1):
            self.use_opt = 0


        # if self.range > 4.5:
        #     x = 0.2
        #
        #
        # else:
        #     self.diffcal2()
        #     if abs(self.delta_R)<1000:
        #         x = self.delta_R*self.k
        #     else:
        #         x = 0.3*self.delta_R/abs(self.delta_R)
              if MOVE == 0:
                  self.twist.linear.x = 0;
                  self.twist.linear.y = 0;
                  self.twist.linear.z = 0
                  self.twist.angular.x = 0;
                  self.twist.angular.y = 0;
                  self.twist.angular.z = 0

              else :
                  self.twist.linear.x = self.speed * (self.range-Rd);
                  self.twist.linear.y = -0.15;
                  self.twist.linear.z = 0
                  self.twist.angular.x = 0;
                  self.twist.angular.y = 0;
                  self.twist.angular.z = 0

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
