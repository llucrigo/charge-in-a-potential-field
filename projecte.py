#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 20:57:48 2021

@author: lluc
"""

"""Plots field lines for dipole."""

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


config=getFileData("config.txt")

# config=[]

# with open('config.txt','r') as config_file:
# 	data=config_file.readline()
	
# 	for data in config_file:
# 		if data.startswith('#'):
# 			data.rstrip()
# 		else:
# 			config.append(float(data.rstrip()))

#print(config)


XMIN, XMAX = config[0],config[1]
YMIN, YMAX = config[2],config[3]
ZOOM = config[4]
XOFFSET = config[5]


electrostatics.init(XMIN, XMAX, YMIN, YMAX, ZOOM, XOFFSET)


charges1=[]
with open('charges.txt','r') as charges_file:
	
	info=charges_file.readline()
	
	for info in charges_file:
		if info.startswith('#'):
			info.rstrip()
		else:
			charges1.append(float(info.rstrip()))

#print(len(charges1))
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
MobileCharge=[]
with open('mobilecharge.txt','r') as mobilecharge_file:
	
	carac=mobilecharge_file.readline()
	
	for carac in mobilecharge_file:
		if carac.startswith('#'):
			carac.rstrip()
		else:
			MobileCharge.append(float(carac.rstrip()))

#print(MobileCharge)
q_mc=MobileCharge[0]
m_mc=MobileCharge[1]
x_mc=MobileCharge[2]
y_mc=MobileCharge[3]
vx_mc=MobileCharge[4]
vy_mc=MobileCharge[5]
h=1e-1


## Plotting ##

# Electric field lines and potential contours

fig = plt.figure(figsize=(6, 4.5))
potential.plot()
field.plot()

n=0
while n<500:
	plt.scatter(x_mc,y_mc, 2, "#00ff00")
	E=field.vector([x_mc,y_mc])
	ac=q_mc*E/m_mc
	x_mc=x_mc+vx_mc*h+(ac[0]/2)*h**2
	vx_mc=vx_mc+ac[0]*h
	y_mc=y_mc+vy_mc*h+(ac[1]/2)*h**2
	vy_mc=vy_mc+ac[1]*h
	n=n+1

for charge in charges:
		charge.plot()
finalize_plot()


plt.show()

