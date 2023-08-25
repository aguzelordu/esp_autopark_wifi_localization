# -*- coding: utf-8 -*-

import math
from math import sin, cos, sqrt, atan2, radians, pi
import pandas as pd
import csv
from math import pow
import numpy as np
import matplotlib.pyplot as plot
import os

fname = os.getcwd()

rssi_data = pd.read_csv(fname+"\\rssi1.csv").values.flatten()

rssi_data = np.flip(rssi_data)
i = np.arange(0, rssi_data.size, 1)
rssi_arr_1 = np.genfromtxt(fname+"\\rssi1.csv", delimiter=',')
rssi_arr_2 = np.genfromtxt(fname+"\\rssi2.csv", delimiter=',')
rssi_arr_3 = np.genfromtxt(fname+"\\rssi3.csv", delimiter=',')


n=1.8 # beta değeri
a=-53 # alpha değeri
def calc_rss(n,d,a):
   cal_rss= (-10*n*(math.log(d, 10)))+a
   print(cal_rss)

def calc_dist(rss,a,n):
    cal_d= pow(10,((rss-a)/(-10*n)))
    return cal_d

dist_arr_1 = []
dist_arr_2 = []
dist_arr_3 = []

for x in rssi_arr_1:
  cal_d = calc_dist(x,a,n)
  dist_arr_1 = np.append(dist_arr_1,cal_d)
for x in rssi_arr_2:
  cal_d = calc_dist(x,a,n)
  dist_arr_2 = np.append(dist_arr_2,cal_d)
for x in rssi_arr_3:
  cal_d = calc_dist(x,a,n)
  dist_arr_3 = np.append(dist_arr_3,cal_d)

rssi_var1 = np.nanvar(rssi_arr_1)
rssi_var2 = np.nanvar(rssi_arr_2)
rssi_var3 = np.nanvar(rssi_arr_3)

print("variance of rssi of beacons are respectively=",rssi_var1,rssi_var2,rssi_var3)


mean_1 = np.nanmean(dist_arr_1)
mean_2 = np.nanmean(dist_arr_2)
mean_3 = np.nanmean(dist_arr_3)

print("distance of tag from reference point 1=",mean_1)
print("distance of tag from reference point 2=",mean_2)
print("distance of tag from reference point 3=",mean_3)

fig = plot.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)


ax1.plot(dist_arr_1)
ax1.axhline(y=mean_1, color='g', linestyle='-')
ax1.axhline(y=2.83, color='r', linestyle='-')

ax2.plot(dist_arr_2)
ax2.axhline(y=mean_2, color='g', linestyle='-')
ax2.axhline(y=1, color='r', linestyle='-')

ax3.plot(dist_arr_3)
ax3.axhline(y=mean_3, color='g', linestyle='-')
ax3.axhline(y=2, color='r', linestyle='-')
plot.show()



def trilateration(x1,y1,r1,x2,y2,r2,x3,y3,r3):
  A = 2*x2 - 2*x1
  B = 2*y2 - 2*y1
  C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
  D = 2*x3 - 2*x2
  E = 2*y3 - 2*y2
  F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
  x = (C*E - F*B) / (E*A - B*D)
  y = (C*D - A*F) / (B*D - A*E)
  return x,y

x,y = trilateration(1.5,1.5,mean_1, 0,0.75,mean_2, 1.5,0,mean_3)

def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)*100 
     dist = round(dist, 2)
     return dist 
print("distance between calculated and setup coordinates=", calculateDistance(0, 0, x, y) ) 
x = round(100*x, 2)
y = round(100*y, 2)

print("calculated cordinates of tag (x,y)=", f"({x} , {y})")

with open("xy_datas.txt", "w") as dosya:
    dosya.write(f"{x}\n{y}")
