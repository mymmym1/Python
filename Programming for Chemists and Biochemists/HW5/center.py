#!/usr/bin/env python
#Yimin

import sys

#Usage: centerpdb.py infile outfile
infile=sys.argv[1]
outfile=sys.argv[2]

#open infile and read into linelist
f1=open(infile, 'r')
linelist=f1.readlines()
f1.close()
 
n=len(linelist)

#Initialize some data
line=[]
xavg=0
yavg=0
zavg=0
atomlist=[]

for i in range(n): 
    line=linelist[i]
    if line[0:4]!="ATOM":    
       continue            #discard lines not start with ATOM

    #parse each line     
    rtype = line[0:6]
    atomnumber = int(line[6:11])
    atomtype = line[12:16]
    altLoc = line[16:17]
    resName = line[17:20]
    chainID = line[21:22]
    resSeq = int(line[22:26])
    iCode = line[26:27]
    x = float(line[30:38])
    y = float(line[38:46])
    z = float(line[46:54])
    occupancy = float(line[54:60])
    tempFactor = float(line[60:66])
    element = line[76:78]
    charge = line[78:80]
 
    #difine dictionary & record data
    atom={'rtype':rtype,
         'atomnumber':atomnumber,
         'atomtype':atomtype,
         'altLoc':altLoc,
         'resName':resName,
         'chainID':chainID,
         'resSeq':resSeq,
         'iCode':iCode,
         'x':x,
         'y':y,
         'z':z,
         'occupancy':occupancy,
         'tempFactor':tempFactor,
         'element':element,
         'charge':charge}
    atomlist.append(atom)
   
#compute geometric center
    xavg+=x
    yavg+=y
    zavg+=z

m=len(atomlist)

xavg=xavg/m
yavg=yavg/m
zavg=zavg/m



#write into outfile with pdb format using new x, y, z
f2=open(outfile,'w')
for atom in atomlist:
   x0=atom['x']-xavg
   y0=atom['y']-yavg
   z0=atom['z']-zavg    
   f2.write("%-6s%5d %-4s%1s%-3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f           %1s%-2s\n" % (atom['rtype'],atom['atomnumber'],atom['atomtype'],atom['altLoc'],atom['resName'],atom['chainID'],atom['resSeq'],atom['iCode'],x0,y0,z0,atom['occupancy'],atom['tempFactor'],atom['element'],atom['charge']))
        
f2.close()
      
print "Done"




