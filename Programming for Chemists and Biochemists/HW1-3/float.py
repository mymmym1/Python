#! /usr/bin/env python

import math

x=raw_input("Please input a float number: ")
x=float(x)
y=int(x)
z=x-y
if z<0.5:
   r=math.floor(x)
else:
   r=math.ceil(x)
print ("This float can be rounded to the nearest integer: ")
print r
