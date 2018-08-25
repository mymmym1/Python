#!/usr/bin/env python
# Yimin

import sys
import masscenter

print "Usage: [infile][outfile][GeoCenter/MassCenter]"

infile = sys.argv[1]
outfile = sys.argv[2]
option=sys.argv[3]

atomlist=[]
atomlist = masscenter.readpdb(infile)        # create list of dictionaries

d={}

if option=="GeoCenter":
        d= masscenter.geocenter(atomlist) # determine center of gravity
        print d
else:
        d= masscenter.masscen(atomlist) # determine center of mass
        print d


print "\nDone!\n"
