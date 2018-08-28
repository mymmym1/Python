#!/usr/bin/env python



import sys

print sys.argv
inname=sys.argv[1]
f=open(inname,'r')
l=f.readlines()
f.close()

outname=sys.argv[2]
f2=open(outname,'w')
for n in l[:3]:
         f2.write(n)
f2.close()


print "Done!"
