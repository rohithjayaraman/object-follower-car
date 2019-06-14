#!/usr/bin/env python

import os
import time
import re
import rospy
import numpy as np
import subprocess 
import carController
import boundingbox
import kalman_filter
import coordinates
from std_msgs.msg import String
from std_msgs.msg import Int16
from sensor_msgs.msg import Joy

class runner(object):
	def __init__(self):
		#self.c=carController.carController()
		self.box=boundingbox.boundingBox()
		self.lastbox1=boundingbox.boundingBox()
		self.lastbox2=boundingbox.boundingBox()
		self.lastbox3=boundingbox.boundingBox()
		self.lastbox4=boundingbox.boundingBox()
		self.lastbox5=boundingbox.boundingBox()
		self.empty=boundingbox.boundingBox()
		self.empty.setPrediction(1)
		self.car=boundingbox.carCharacteristics()
		self.flag=0
		self.pred=""
		#min_area=10000.0
		#max_area=42000.0
		self.check=0
		self.time=rospy.get_time()
		self.rtime=0.0
		self.input=""
		self.count=0
		self.sub=rospy.Subscriber("/detectnet/detections", String, self.callback)
		self.sub2=rospy.Subscriber("joy", Joy, self.callback2)
		self.manualControl=0
		self.kf=kalman_filter.kalman_filter(1023,0.125,32,0)
	
	def callback(self, data):
		if(self.manualControl==0):		
			self.input=str(data)
			self.input=self.input[7:-1]
			#print self.input	
			self.check=1
			self.lastbox1.set(self.lastbox2)
			self.lastbox2.set(self.lastbox3)
			self.lastbox3.set(self.lastbox4)
			self.lastbox4.set(self.lastbox5)	
			if self.check==1:		
				if(re.search("BoundingBox:",self.input)):						
					index=self.input.find("BoundingBox:")
					#print self.input				
					self.lastbox5.set(self.input)
					self.box.set(self.lastbox5)
					if(self.box.getConfidence()<0.4):
						flag=2
						self.lastbox5.set(self.empty)
						self.box.set(self.lastbox4)				
					else:
						flag=1				
				elif(re.search("NoBoundingBox",self.input)):
					self.lastbox5.set(self.empty)
					flag=2
				else:
					print "Ideally, should not reach here"				
			else:
				flag=3		
			box_decision=0
			no_box_decision=0	
			if(self.lastbox1.getPrediction()==1):
				no_box_decision+=1
			elif(self.lastbox1.getPrediction()==2):
				box_decision+=1
			if(self.lastbox2.getPrediction()==1):
				no_box_decision+=1
			elif(self.lastbox2.getPrediction()==2):
				box_decision+=1
			if(self.lastbox3.getPrediction()==1):
				no_box_decision+=1
			elif(self.lastbox3.getPrediction()==2):
				box_decision+=1
			if(self.lastbox4.getPrediction()==1):
				no_box_decision+=1
			elif(self.lastbox4.getPrediction()==2):
				box_decision+=1	
			if(self.lastbox5.getPrediction()==1):
				no_box_decision+=1
			elif(self.lastbox5.getPrediction()==2):
				box_decision+=1
			if(box_decision>=3):
				self.car.calculateMaxSteer(self.lastbox5)
				self.car.calculateMaxThrottle(self.lastbox5)
				h=254.6/(self.box.getHeight()*0.04)			
				h_filtered=self.kf.getValue(h)
				if(h_filtered<25):
					self.car.setStopCharacteristics(0,0)
				self.pred=" Box Predicted    | "
			elif(no_box_decision>=3):
				self.car.setStopCharacteristics(0,0)	
				h=self.kf.getX()
				h_filtered=self.kf.getValue(h)
				self.pred=" No Box Predicted | "
			self.car.setSteer()
			self.car.setThrottle(self.box)
			#c.set(car.getActualSteer(),car.getActualThrottle())
			#print flag
			if(flag==1):
				print "%.2f" % (rospy.get_time()-self.time)," | ",
				print "Box detected   |",self.pred, 
				if(self.pred==" Box Predicted    | "):
					print self.car.getDetails(),
					print " | ",self.box.getCoordinates()
				else:
					print self.car.getDetails()
			elif(flag==2):
				print "%.2f" % (rospy.get_time()-self.time)," | ",		
				print "No Box detected|",self.pred,
				if(self.pred==" Box Predicted    | "):
					print self.car.getDetails(),
					print " | ",self.box.getCoordinates()
				else:
					print self.car.getDetails()
			elif(flag==3):
				if(self.pred==" Box Predicted    | "):
					print "%.2f" % (rospy.get_time()-self.time)," | ",			
					print "No new data    |",self.pred,
					print self.car.getDetails(),			
					print " | ",self.box.getCoordinates()
	
	def callback2(self,data):
		if(data.buttons[4]==1):
			self.manualControl=1
			print " LB "
			#self.sub.unregister()
		if(data.buttons[6]==1):
			self.manualControl=0
			print " RB "
			self.count=0
			#self.sub=rospy.Subscriber("/detectnet/detections", String, self.callback)
		if(self.manualControl==1):		
			if(data.buttons[8]==1):
				print "Emergency stop"
				self.car.stop()
			if(data.buttons[0]==1):
				self.car.changeTargetThrottle(-1)
				print "pressed 1 ",self.count	
				self.count+=1
			if(data.buttons[1]==1):
				self.car.changeTargetSteer(1)
				print "pressed 2 ",self.count	
				self.count+=1
			if(data.buttons[2]==1):
				self.car.changeTargetSteer(-1)
				print "pressed 3 ",self.count	
				self.count+=1
			if(data.buttons[3]==1):
				self.car.changeTargetThrottle(1)
				print "pressed 4 ",self.count	
				self.count+=1
			if(data.axes[0]==1):
				self.car.changeSteer(-1)
				print "axis x -",self.count
				self.count+=1
			if(data.axes[0]==-1):
				self.car.changeSteer(1)
				print "axis x +",self.count
				self.count+=1	
			if(data.axes[3]==1):
				self.car.changeThrottle(1)
				print "axis y +",self.count
				self.count+=1
			if(data.axes[3]==-1):
				self.car.changeThrottle(-1)
				print "axis y -",self.count
				self.count+=1		
			print self.car.getDetails()
	
	def running(self):
		print "Hello"
		rate = rospy.Rate(100)
		while not rospy.is_shutdown():
			if self.check==0 and self.manualControl==0:
				if(self.pred==" Box Predicted    | "):
					print "%.2f" % (rospy.get_time()-self.time)," | ",			
					print "No new data    |",self.pred,
					print self.car.getDetails(),			
					print " | ",self.box.getCoordinates()
			self.check=0
			rate.sleep()
		rospy.spin()
		

if __name__ == '__main__':
	rospy.init_node("runner", anonymous=True)
	my_node = runner()
	my_node.running()
