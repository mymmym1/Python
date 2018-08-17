#! /usr/bin/env python

s=raw_input("Please input a series of numbers seperated by ',': ")
l=s.split(',')
k=len(l)
a=0
d=0
for n in l:
    a=a+int(n)
a=a/k
print ("The average of the numbers is:" )
print a
for n in l:
    d=d+(int(n)-a)**2
d=(d/k)**0.5
print ("The standard deviation of the numbers is:" )
print d   
