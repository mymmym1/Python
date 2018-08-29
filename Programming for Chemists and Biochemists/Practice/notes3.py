#!/usr/bin/env python

import random, sys

ntests=int(sys.argv[1])
grades=[]
for n in range(ntests):
   grades.append(random.gauss(80,10))
print grades[-1]

a=0
b=0
c=0
d=0
f=0

for n in grades:
    if n>=90:
       a+=1
    elif n>=80:
         b+=1
    elif n>=70:
         c+=1
    elif n>=65:
         d+=1
    else: 
         f+=1
print "As=",'*'*a
print "Bs=",'*'*b
print "Cs=",'*'*c
print "Ds=",'*'*d
print "Fs=",'*'*f

