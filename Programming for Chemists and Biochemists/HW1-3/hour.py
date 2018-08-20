#! /usr/bin/env python

import math

print("Please input time in 24 hour format as 'hh:mm:ss'! ")
hh=raw_input("hours: ")
mm=raw_input("minutes: ")
ss=raw_input("seconds: ")

if int(hh)>24 or int(hh)<0 or int(mm)>60 or int(mm)<0 or int(ss)>60 or int(ss)<0:
   print("Your input is wrong")
   
else:
   print("Your input time is: ")
   print hh + ":" + mm + ":" + ss
   h=raw_input("Please input the hours add to this time: ")
   hour=(int(hh)+int(h))%12
   print("The time in 12 hour format is: ")
   print str(hour) + ":" + mm + ":" + ss
