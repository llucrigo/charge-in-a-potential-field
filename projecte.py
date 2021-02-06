#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 20:57:48 2021
@author: lluc
"""

#from matplotlib import pyplot
import matplotlib.pyplot as plt
import numpy
import os

import electrostatics
from electrostatics import PointCharge, ElectricField, Potential
from electrostatics import finalize_plot

# pylint: disable=invalid-name


def getFileData(filename):
	array=[]
	with open(filename,'r') as data_file:
		info=data_file.readline()
		for info in data_file:
			if info.startswith('#'):
				info.rstrip()
			else:
				array.append(float(info.rstrip()))
	return array


class MobileCharge_class:
	#Charge moving in the electric field

	h=0.1 #Time step
	eps=0.1
	nmax=50

	def __init__(self, electricfield, q, m, r, v):
		self.electricfield= electricfield
		self.q=q
		self.m=m
		self.r=r
		self.v=v

	def move(self):
		E=self.electricfield.vector([self.r[0],self.r[1]])
		ac=self.q*E/self.m
		n=1
		h=self.h
		nr=[0,0]
		while n<self.nmax:
			nr[0]=self.r[0]+self.v[0]*h+(ac[0]/2)*h**2
			nr[1]=self.r[1]+self.v[1]*h+(ac[1]/2)*h**2
			d=((nr[0]-self.r[0])**2+(nr[1]-self.r[1])**2)**.5
			if (d<self.eps):
				self.r=nr
				self.v[0]=self.v[0]+ac[0]*h
				self.v[1]=self.v[1]+ac[1]*h
				return n
			else:
				h=h/2
			n=n+1
		self.r=nr
		self.v[0]=self.v[0]+ac[0]*h
		self.v[1]=self.v[1]+ac[1]*h
		return n

	def get_r(self):
		return self.r

	def plot(self,color):
		plt.scatter(self.r[0],self.r[1], 1, color)

	def checkpoint(self,xmin, xmax, ymin, ymax):
		if self.r[0]>xmax or self.r[0]<xmin or self.r[1]>ymax or self.r[1]<ymin:
			return True


config=getFileData("config.txt")

XMIN, XMAX, YMIN, YMAX, ZOOM, XOFFSET=config


electrostatics.init(XMIN, XMAX, YMIN, YMAX, ZOOM, XOFFSET)

charges1=getFileData("charges.txt")

a=int(len(charges1)/3)
#print(a)

chargedata=[]
for i in range(0,a):
	a=charges1[i*3],[charges1[i*3+1],charges1[i*3+2]]
	chargedata.append(a)


#print(chargedata)
# Set up the charges, electric field, and potential

charges=[]

for i in range(0,len(chargedata)):
	b=PointCharge(chargedata[i][0],chargedata[i][1])
	charges.append(b)
#print(charges)



field = ElectricField(charges)
potential = Potential(charges)


#MobileCharge
MobileCharge=getFileData("mobilecharge.txt")

#print(MobileCharge)

q_mc=[]
m_mc=[]
x_mc=[]
y_mc=[]
vx_mc=[]
vy_mc=[]
mobilecharge=[]

for i in range(0, int(len(MobileCharge)/6)): 
	q_mc.append(MobileCharge[i*6])
	m_mc.append(MobileCharge[i*6+1])
	x_mc.append(MobileCharge[i*6+2])
	y_mc.append(MobileCharge[i*6+3])
	vx_mc.append(MobileCharge[i*6+4])
	vy_mc.append(MobileCharge[i*6+5])
	mobilecharge.append(MobileCharge_class(field,q_mc[i],m_mc[i],[x_mc[i],y_mc[i]],[vx_mc[i],vy_mc[i]]))

## Plotting ##

colors=["#00ff00","#ff0000","#0000ff","#f00f00","#0f00f0","#00f00f"]

# Electric field lines and potential contours

fig = plt.figure(figsize=(6, 4.5))
potential.plot()
field.plot()

for i in range(0, len(mobilecharge)):
	n=0
	while n<500:
		if mobilecharge[i].checkpoint(XMIN, XMAX, YMIN, YMAX):
			break
		else:
			x_mc,y_mc=mobilecharge[i].get_r()
			mobilecharge[i].plot(colors[i])
			m=mobilecharge[i].move()
			r=mobilecharge[i].get_r()
			#print(n,m,r)
			n=n+1
	print(i, n)

for charge in charges:
		charge.plot()
finalize_plot()

plt.show()
