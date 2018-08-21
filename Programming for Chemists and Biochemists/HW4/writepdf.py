#/usr/bin/env python

#Yimin Miao

import sys

print sys.argv
inname=sys.argv[1]

f=open(inname,'r')
l=f.readlines()
f.close()

outname=sys.argv[3]
f2=open(outname,'w')
n = int(sys.argv[2]) -1
f2.write(l[n])
f2.close()

print l[n]
